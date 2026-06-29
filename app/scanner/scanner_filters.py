class ScannerFilters:

    @staticmethod
    def price_filter(price: float) -> bool:

        return price >= 100

    @staticmethod
    def volume_filter(volume_ratio: float) -> bool:

        return volume_ratio >= 1.5

    @staticmethod
    def risk_reward(rr: float) -> bool:

        return rr >= 2
