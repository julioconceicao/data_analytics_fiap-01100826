"""Análise mensal dos pedidos da Olist."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ModuleNotFoundError as exc:
    raise SystemExit(
        f"Dependencia ausente: {exc.name}. "
        "Instale os pacotes com: pip install pandas numpy matplotlib"
    ) from exc


BLUE = "#1F4E78"
GREEN = "#2E8B57"
ORANGE = "#E67E22"
GRAY = "#6B7280"

ORDERS_FILENAME = "olist_orders_dataset.csv"
ITEMS_FILENAME = "olist_order_items_dataset.csv"


def configure_plotting() -> None:
    """Configura os gráficos."""
    plt.style.use("seaborn-v0_8-whitegrid")
    pd.options.display.float_format = "{:,.2f}".format


def parse_args() -> argparse.Namespace:
    """Lê os argumentos."""
    parser = argparse.ArgumentParser(
        description=(
            "Calcula a evolucao mensal de pedidos, receita e ticket medio da Olist."
        )
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Pasta que contem os arquivos CSV da Olist.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "outputs" / "figures",
        help="Pasta de saida (padrao: ./outputs/figures).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Exibe os graficos na tela alem de salva-los.",
    )
    return parser.parse_args()


def find_data_dir(data_dir: Path | None) -> Path:
    """Procura a pasta dos dados."""
    if data_dir is not None:
        candidates = [data_dir.expanduser()]
    else:
        script_dir = Path(__file__).resolve().parent
        candidates = [
            Path.cwd() / "dataset",
            Path.cwd().parent / "dataset",
            script_dir / "dataset",
            script_dir.parent / "dataset",
        ]

    # Evita caminhos repetidos.
    unique_candidates = list(dict.fromkeys(path.resolve() for path in candidates))
    required_files = (ORDERS_FILENAME, ITEMS_FILENAME)

    for candidate in unique_candidates:
        if all((candidate / filename).is_file() for filename in required_files):
            return candidate

    checked = "\n  - ".join(str(path) for path in unique_candidates)
    raise FileNotFoundError(
        "Nao foi encontrada uma pasta com os dois CSVs necessarios. "
        "Informe o caminho com --data-dir.\n"
        f"Locais verificados:\n  - {checked}"
    )


def load_and_prepare_data(data_dir: Path) -> pd.DataFrame:
    """Lê e prepara os dados."""
    orders = pd.read_csv(
        data_dir / ORDERS_FILENAME,
        usecols=["order_id", "order_status", "order_purchase_timestamp"],
        parse_dates=["order_purchase_timestamp"],
    )
    items = pd.read_csv(
        data_dir / ITEMS_FILENAME,
        usecols=["order_id", "price"],
    )

    revenue_by_order = (
        items.groupby("order_id", as_index=False).agg(revenue=("price", "sum"))
    )
    analysis = (
        orders.loc[orders["order_status"].eq("delivered")]
        .merge(revenue_by_order, on="order_id", how="inner", validate="one_to_one")
        .copy()
    )

    if analysis.empty:
        raise ValueError("Nenhum pedido entregue com itens associados foi encontrado.")

    analysis["month"] = (
        analysis["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    )
    return analysis


def calculate_monthly_metrics(analysis: pd.DataFrame) -> pd.DataFrame:
    """Calcula os dados por mês."""
    monthly = (
        analysis.groupby("month", as_index=False)
        .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
        .sort_values("month")
        .reset_index(drop=True)
    )
    monthly["ticket"] = monthly["revenue"] / monthly["orders"]
    monthly["mom_orders"] = monthly["orders"].pct_change()
    monthly["mom_revenue"] = monthly["revenue"].pct_change()
    monthly["mom_ticket"] = monthly["ticket"].pct_change()

    # Busca os dados do ano anterior.
    prior = monthly[["month", "orders", "revenue", "ticket"]].copy()
    prior["month"] = prior["month"] + pd.DateOffset(years=1)
    prior = prior.rename(
        columns={name: f"prior_{name}" for name in ["orders", "revenue", "ticket"]}
    )
    monthly = monthly.merge(prior, on="month", how="left", validate="one_to_one")

    for metric in ["orders", "revenue", "ticket"]:
        monthly[f"yoy_{metric}"] = (
            monthly[metric] / monthly[f"prior_{metric}"] - 1
        )

    return monthly


def finish_figure(
    fig: plt.Figure,
    output_path: Path,
    show: bool,
    *,
    tight_rect: tuple[float, float, float, float] | None = None,
) -> None:
    """Salva e mostra o gráfico."""
    if tight_rect is None:
        fig.tight_layout()
    else:
        fig.tight_layout(rect=tight_rect)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def plot_monthly_evolution(
    monthly: pd.DataFrame, output_dir: Path, show: bool
) -> None:
    """Cria o gráfico mensal."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True)

    axes[0].plot(
        monthly["month"], monthly["orders"], marker="o", lw=2.2, color=BLUE
    )
    axes[0].set_title("Pedidos entregues por mes", loc="left", weight="bold")
    axes[0].set_ylabel("Pedidos")

    axes[1].plot(
        monthly["month"],
        monthly["revenue"] / 1_000_000,
        marker="o",
        lw=2.2,
        color=GREEN,
    )
    axes[1].set_title("Receita mensal de produtos", loc="left", weight="bold")
    axes[1].set_ylabel("R$ milhoes")

    # Ignora 2016 por ter poucos pedidos.
    ticket_plot = monthly["ticket"].where(
        monthly["month"] >= pd.Timestamp("2017-01-01")
    )
    axes[2].plot(
        monthly["month"], ticket_plot, marker="o", lw=2.2, color=ORANGE
    )
    axes[2].set_title("Ticket medio mensal", loc="left", weight="bold")
    axes[2].set_ylabel("R$ por pedido")

    for axis in axes:
        axis.axvspan(
            pd.Timestamp("2016-09-01"),
            pd.Timestamp("2016-12-31"),
            alpha=0.08,
            color=ORANGE,
        )
        axis.axvspan(
            pd.Timestamp("2017-11-01"),
            pd.Timestamp("2017-11-30"),
            alpha=0.10,
            color="black",
        )
        axis.tick_params(axis="x", rotation=45)

    fig.suptitle(
        "Olist: evolucao mensal de volume, receita e ticket medio",
        fontsize=16,
        weight="bold",
    )
    finish_figure(
        fig,
        output_dir / "01_evolucao_mensal.png",
        show,
        tight_rect=(0, 0.03, 1, 0.97),
    )


def plot_growth_index(
    monthly: pd.DataFrame, output_dir: Path, show: bool
) -> None:
    """Compara o crescimento desde 2017."""
    comparable = monthly.loc[
        monthly["month"].between("2017-01-01", "2018-08-01")
    ].copy()
    if comparable.empty:
        raise ValueError("Nao ha dados entre janeiro de 2017 e agosto de 2018.")

    fig, axis = plt.subplots(figsize=(14, 6))
    axis.plot(
        comparable["month"],
        comparable["orders"] / comparable["orders"].iloc[0] * 100,
        label="Pedidos",
        color=BLUE,
        lw=2.5,
    )
    axis.plot(
        comparable["month"],
        comparable["revenue"] / comparable["revenue"].iloc[0] * 100,
        label="Receita",
        color=GREEN,
        lw=2.5,
    )
    axis.plot(
        comparable["month"],
        comparable["ticket"] / comparable["ticket"].iloc[0] * 100,
        label="Ticket medio",
        color=ORANGE,
        lw=2.5,
    )
    axis.axhline(100, color=GRAY, lw=1)
    axis.set_title(
        "Crescimento acumulado: volume e receita avancam juntos",
        loc="left",
        weight="bold",
    )
    axis.set_ylabel("Indice (jan/2017 = 100)")
    axis.legend(ncol=3, frameon=False)
    axis.tick_params(axis="x", rotation=45)
    finish_figure(fig, output_dir / "02_indice_crescimento.png", show)


def plot_annual_growth(
    monthly: pd.DataFrame, output_dir: Path, show: bool
) -> None:
    """Mostra o crescimento anual."""
    growth = monthly.loc[
        monthly["month"].between("2018-03-01", "2018-08-01")
    ].copy()
    if growth.empty:
        raise ValueError("Nao ha dados entre marco e agosto de 2018.")

    x_positions = np.arange(len(growth))
    width = 0.36

    fig, axis = plt.subplots(figsize=(13, 6))
    axis.bar(
        x_positions - width / 2,
        growth["yoy_orders"] * 100,
        width,
        label="Pedidos",
        color=BLUE,
    )
    axis.bar(
        x_positions + width / 2,
        growth["yoy_revenue"] * 100,
        width,
        label="Receita",
        color=GREEN,
    )
    axis.plot(
        x_positions,
        growth["yoy_ticket"] * 100,
        color=ORANGE,
        marker="o",
        lw=2.5,
        label="Ticket medio",
    )
    axis.set_xticks(x_positions, growth["month"].dt.strftime("%b/%Y"))
    axis.set_ylabel("Variacao contra o mesmo mes de 2017 (%)")
    axis.set_title(
        "Desaceleracao das taxas anuais entre marco e agosto de 2018",
        loc="left",
        weight="bold",
    )
    axis.axhline(0, color=GRAY, lw=1)
    axis.legend(ncol=3, frameon=False)
    finish_figure(fig, output_dir / "03_crescimento_anual_2018.png", show)


def period_summary(
    analysis: pd.DataFrame, start: str, end: str
) -> pd.Series:
    """Resume os dados do período."""
    frame = analysis.loc[analysis["month"].between(start, end)]
    orders_count = frame["order_id"].nunique()
    if orders_count == 0:
        raise ValueError(f"Nao ha pedidos entre {start} e {end}.")

    revenue = frame["revenue"].sum()
    return pd.Series(
        {
            "pedidos": orders_count,
            "receita": revenue,
            "ticket_medio": revenue / orders_count,
        }
    )


def print_comparable_summary(analysis: pd.DataFrame) -> None:
    """Compara os dois anos."""
    summary = pd.DataFrame(
        {
            "jan-ago/2017": period_summary(
                analysis, "2017-01-01", "2017-08-01"
            ),
            "jan-ago/2018": period_summary(
                analysis, "2018-01-01", "2018-08-01"
            ),
        }
    ).T
    growth_summary = summary.loc["jan-ago/2018"] / summary.loc["jan-ago/2017"] - 1

    print("\nResumo comparavel:")
    print(summary.to_string())
    print("\nVariacao 2018 vs. 2017:")
    print(growth_summary.rename("variacao").to_frame().to_string())


def main() -> None:
    """Executa o programa."""
    args = parse_args()
    configure_plotting()

    data_dir = find_data_dir(args.data_dir)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Dataset: {data_dir}")
    print(f"Saidas: {output_dir}")

    analysis = load_and_prepare_data(data_dir)
    monthly = calculate_monthly_metrics(analysis)

    print(f"Pedidos entregues: {analysis['order_id'].nunique():,}")
    print(f"Receita total: R$ {analysis['revenue'].sum():,.2f}")

    plot_monthly_evolution(monthly, output_dir, args.show)
    plot_growth_index(monthly, output_dir, args.show)
    plot_annual_growth(monthly, output_dir, args.show)
    print_comparable_summary(analysis)

    csv_path = output_dir / "indicadores_mensais.csv"
    monthly.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print("\nArquivos gerados:")
    for output_path in sorted(output_dir.iterdir()):
        if output_path.is_file():
            print(f"- {output_path}")


if __name__ == "__main__":
    main()
