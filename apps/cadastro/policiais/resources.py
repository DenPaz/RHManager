from import_export import resources

from .models import Policial


class PolicialResource(resources.ModelResource):
    class Meta:
        model = Policial
        exclude = (
            "id",
            "created",
            "modified",
        )
        import_id_fields = ["matricula", "cpf"]
        skip_unchanged = True
        report_skipped = True
        clean_model_instances = True


# class PolicialResource(resources.ModelResource):
#     def before_import(self, dataset, using_transactions, dry_run, **kwargs):
#         required_fields = [
#             field.name
#             for field in Policial._meta.get_fields()
#             if (not field.null and not field.blank)
#             and field.name not in ["created", "modified"]
#         ]
#         missing_fields = set(required_fields) - set(dataset.headers)

#         if missing_fields:
#             raise ValidationError(
#                 f"Os seguintes campos obrigatórios não foram encontrados: {missing_fields}"
#             )

#     class Meta:
#         model = Policial
#         fields = None
#         exclude = ["created", "modified"]

#         import_id_fields = ["matricula"]
