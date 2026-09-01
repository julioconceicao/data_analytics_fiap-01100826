# import kagglehub
# from kagglehub import KaggleDatasetAdapter
# import os 

# user = os.getlogin()
# # Caminho do arquivo que vamos analisar (Nesse caso aqui, é a lista de Pedidos)
# # Não se esqueçam de trocar o local do arquivo para o caminho local de vocês.
# #{user} é o nome do usuário do windows que está acessando
# file_path = fr"C:\Users\{user}\Documents\fiap\data_analytics_fiap-01100826\dataset\olist_orders_dataset.csv"

# # Load the latest version
# df = kagglehub.load_dataset(
#   KaggleDatasetAdapter.PANDAS,
#   "olistbr/brazilian-ecommerce",
#   file_path,
#   # Provide any additional arguments like 
#   # sql_query or pandas_kwargs. See the 
#   # documenation for more information:
#   # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
# )

# print("First 5 records:", df.head())