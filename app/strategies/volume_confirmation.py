class VolumeConfirmation:

    def relative_volume(self, current_volume, avg_volume):

        if avg_volume == 0:
            return 0

        return current_volume / avg_volume

    def is_valid(self, current_volume, avg_volume):

        return self.relative_volume(
            current_volume,
            avg_volume
        ) >= 1.5
