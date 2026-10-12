from langchain_community.document_loaders import CSVLoader

file_path = "assets/有错误的比赛.csv"
csv = CSVLoader(file_path).load()
print(csv)
