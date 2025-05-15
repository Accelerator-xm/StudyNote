from langserve import RemoteRunnable

if __name__ == "__main__":
    client = RemoteRunnable("http://127.0.0.1:8000/chain/")
    print(client.invoke({
        "language":"日语",
        "text":"你好"
    }))