from query_process import QueryProcessor

def test_QueryProcessor():
    file = open('test_document.txt', 'rt')
    text = file.read()
    file.close()
    qp = QueryProcessor()
    results = qp.process(text)
    print(results)
