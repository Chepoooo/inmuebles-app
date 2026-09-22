from inventory.models import Inventory
from inventory.defaults import INVENTORY_SECTION_DEFINITIONS


def save_inventory_from_post(request, inventory):
    sections = inventory.sections.prefetch_related("items").all()

    for section in sections:

        for item in section.items.all():

            if item.is_description:

                item.description = request.POST.get(
                    f"description_{item.id}",
                    "",
                ).strip()

                item.save(
                    update_fields=[
                        "description",
                    ]
                )

                continue

            status = request.POST.get(
                f"status_{item.id}",
                "",
            ).strip()

            item_type = request.POST.get(
                f"item_type_{item.id}",
                "",
            ).strip()

            description = request.POST.get(
                f"description_{item.id}",
                "",
            ).strip()

            base_section_name = section.name

            if section.name.startswith("Alcoba auxiliar "):
                base_section_name = "Alcoba auxiliar"

            elif section.name.startswith("Baño auxiliar "):
                base_section_name = "Baño auxiliar"

            extra_fields = {}

            for section_name, definitions in INVENTORY_SECTION_DEFINITIONS.items():

                if base_section_name == section_name:

                    for definition in definitions:

                        if definition["name"] == item.name:

                            extra_fields = definition.get(
                                "extra_fields",
                                {},
                            )

                            break

            extra_data = {}

            for field_name in extra_fields:

                value = request.POST.get(
                    f"extra_{field_name}_{item.id}",
                    "",
                ).strip()

                extra_data[field_name] = value

            item.status = status
            item.item_type = item_type
            item.description = description
            item.extra_data = extra_data

            item.save(
                update_fields=[
                    "status",
                    "item_type",
                    "description",
                    "extra_data",
                ]
            )