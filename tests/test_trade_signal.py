from app.scanner.scanner_executor import ScannerExecutor

scanner = ScannerExecutor()

trade = scanner.scan("BEL.NS")

print(trade)
