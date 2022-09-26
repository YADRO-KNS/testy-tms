class DtoMixin:
    dto_class = None

    def get_dto_class(self):
        assert self.dto_class is not None, (
            "'%s' should either include a `dto_class` attribute, "
            "or override the `get_dto_class()` method."
            % self.__class__.__name__
        )

        return self.dto_class

    def build_dto_from_validated_data(self, validated_data):
        dto_class = self.get_dto_class()
        return dto_class(**validated_data)
