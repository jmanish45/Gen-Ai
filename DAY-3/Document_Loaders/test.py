from langchain_community.document_loaders import TextLoader 
#document_loaders are used to load documents from various sources and formats into a format that can be processed by language models. They help in reading and parsing text data from files, databases, web pages, and other sources, making it easier to work with unstructured data in natural language processing tasks.

loader = TextLoader("./notes.txt",encoding="utf-8")
#loader is an instance of the TextLoader class, which is initialized with the path to a text file ("./notes.txt"). This loader will read the contents of the specified text file and prepare it for further processing or analysis.

docs = loader.load()
#docs is a variable that stores the loaded documents from the text file. The load() method of the TextLoader class reads the contents of the specified text file and returns it in a structured format, typically as a list of document objects or strings, depending on the implementation of the loader.

print(docs[0])
#it prints the representation of the docs object, which contains the loaded documents from the text file. This output will typically include the content of the loaded documents, confirming that the text file has been successfully loaded and is ready for further use.

