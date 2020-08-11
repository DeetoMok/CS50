import requests

def main():
    # response = response from this website
    res = requests.get("https://www.google.com/")
    # Print the text of whatever this response is
    print(res.text)

if __name__ == "__main__":
    main()
