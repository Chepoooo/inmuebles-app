INVENTORY_SECTION_DEFINITIONS = {

    "Entrada": [
        {
            "name": "Puerta",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámpara",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Sala - comedor": [
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorrientes",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Balcón": [
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorrientes",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Baranda",
            "type_options": [
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Cocina": [
        {
            "name": "Puerta de entrada",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Lavaplatos",
        },
        {
            "name": "Grifería",
            "type_options": [
                "Aluminio",
                "Plástico",
            ],
        },
        {
            "name": "Muebles flotante",
        },
        {
            "name": "Muebles inferiores",
        },
        {
            "name": "Mesón",
            "type_options": [
                "Mármol",
                "Granito",
                "Cerámica",
            ],
        },
        {
            "name": "Estufa",
            "type_options": [
                "Empotrada de vidrio",
                "Empotrada de aluminio",
            ],
        },
        {
            "name": "Horno",
        },
        {
            "name": "Campana extractora",
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Área de labores": [
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Llaves de agua",
            "type_options": [
                "Plástico",
                "Aluminio",
                "Cobre",
            ],
        },
        {
            "name": "Llaves de gas",
        },
        {
            "name": "Cifones",
            "type_options": [
                "Plástico",
                "Aluminio",
            ],
        },
        {
            "name": "Lavadero",
            "type_options": [
                "Piedra",
                "PVC",
            ],
        },
        {
            "name": "Caja de tacos",
            "type_options": [
                "Tapa en aluminio",
                "Tapa en plástico",
                "Sin tapa",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Hall de alcobas": [
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Alcoba principal": [
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Clóset",
            "type_options": [
                "Empotrado en madera",
                "Sin empotrar",
            ],
        },
        {
            "name": "Vestier",
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Alcoba auxiliar": [
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Clóset",
        },
        {
            "name": "Vestier",
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Baño principal": [
        {
            "name": "Puerta de entrada",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Pared de baño",
            "type_options": [
                "Enchapadas",
                "Pintadas",
            ],
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Lavamanos",
            "type_options": [
                "Sencillo",
                "Sobre mueble de madera",
            ],
        },
        {
            "name": "Inodoro",
            "type_options": [
                "Sencillo",
                "Con marco",
                "Flotante",
            ],
        },
        {
            "name": "División de ducha",
            "type_options": [
                "Vidrio",
                "Aluminio",
            ],
        },
        {
            "name": "Ducha",
            "type_options": [
                "Plástico",
                "Aluminio",
            ],
        },
        {
            "name": "Jabonera",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Porta papel",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Toalleros",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Baño auxiliar": [
        {
            "name": "Puerta de entrada",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Pared de baño",
            "type_options": [
                "Enchapadas",
                "Pintadas",
            ],
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Ventanas",
            "type_options": [
                "Aluminio y vidrio",
            ],
        },
        {
            "name": "Lavamanos",
            "type_options": [
                "Sencillo",
                "Sobre mueble de madera",
            ],
        },
        {
            "name": "Inodoro",
            "type_options": [
                "Sencillo",
                "Con marco",
                "Flotante",
            ],
        },
        {
            "name": "División de ducha",
            "type_options": [
                "Vidrio",
                "Aluminio",
            ],
        },
        {
            "name": "Ducha",
            "type_options": [
                "Plástico",
                "Aluminio",
            ],
        },
        {
            "name": "Jabonera",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Porta papel",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Toalleros",
            "type_options": [
                "Aluminio",
                "Plástico",
                "Cerámica",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Alcoba y baño de servicio": [
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],

    "Patio": [
        {
            "name": "Puertas",
            "type_options": [
                "Madera",
                "Hierro",
                "Aluminio",
                "Vidrio",
            ],
        },
        {
            "name": "Pisos",
            "type_options": [
                "Cerámica",
                "Mármol",
                "Madera",
                "Granito",
            ],
        },
        {
            "name": "Paredes",
            "extra_fields": {
                "painted": {
                    "label": "¿Está pintada?",
                    "type": "select",
                    "options": [
                        "Sí",
                        "No",
                    ],
                },
                "paint_color": {
                    "label": "Color de pintura",
                    "type": "text",
                },
            },
        },
        {
            "name": "Lámparas",
            "type_options": [
                "Bombillo",
                "LED",
                "Colgante",
            ],
        },
        {
            "name": "Tomacorriente",
            "type_options": [
                "Doble",
                "Doble de seguridad",
                "Mixto",
            ],
        },
        {
            "name": "Interruptores",
            "type_options": [
                "Sencillo",
                "Doble",
            ],
        },
        {
            "name": "Descripción adicional",
            "is_description": True,
        },
    ],
}