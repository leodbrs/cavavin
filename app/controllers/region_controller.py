from app.models.Region import Region


class RegionController(Region):
    @staticmethod
    def get_by_id(region_id):
        """
        Get a region by its ID.
        """
        return Region.query.get(region_id)

    @staticmethod
    def get_all():
        """
        Get all regions.
        """
        return Region.query.all()
