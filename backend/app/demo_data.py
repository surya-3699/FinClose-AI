def demo_data():
    settlements = [
        {"id":"S001","reference":"pay_1001","amount":1200.0,"date":"2026-08-01","customer":"Acme","source":"settlement"},
        {"id":"S002","reference":"pay_1002","amount":850.0,"date":"2026-08-02","customer":"Nova","source":"settlement"},
        {"id":"S003","reference":"PAY-1003-A","amount":2100.0,"date":"2026-08-03","customer":"Zen","source":"settlement"},
        {"id":"S004","reference":"pay1004","amount":500.0,"date":"2026-08-05","customer":"Orbit","source":"settlement"},
        {"id":"S005","reference":"missing-999","amount":750.0,"date":"2026-08-05","customer":"Unknown","source":"settlement"},
        {"id":"S006","reference":"ord-7006","amount":1999.0,"date":"2026-08-06","customer":"Pulse","source":"settlement"},
        {"id":"S007","reference":"transfer-A17","amount":3200.0,"date":"2026-08-07","customer":"Aster","source":"settlement"},
        {"id":"S008","reference":"invoice-88","amount":640.0,"date":"2026-08-08","customer":"Brix","source":"settlement"},
    ]
    ledger = [
        {"id":"L001","reference":"pay_1001","amount":1200.0,"date":"2026-08-01","customer":"Acme","source":"ledger"},
        {"id":"L002","reference":"pay_1002","amount":850.0,"date":"2026-08-02","customer":"Nova","source":"ledger"},
        {"id":"L003","reference":"pay1003a","amount":2100.0,"date":"2026-08-04","customer":"Zen","source":"ledger"},
        {"id":"L004","reference":"pay-1004","amount":500.0,"date":"2026-08-06","customer":"Orbit","source":"ledger"},
        {"id":"L005","reference":"order7006","amount":1999.0,"date":"2026-08-07","customer":"Pulse","source":"ledger"},
        {"id":"L006","reference":"transfera17x","amount":3200.0,"date":"2026-08-11","customer":"Aster","source":"ledger"},
        {"id":"L007","reference":"invoice88","amount":640.0,"date":"2026-08-08","customer":"Brix","source":"ledger"},
        {"id":"L008","reference":"manual-entry","amount":420.0,"date":"2026-08-09","customer":"Internal","source":"ledger"},
    ]
    return settlements, ledger
