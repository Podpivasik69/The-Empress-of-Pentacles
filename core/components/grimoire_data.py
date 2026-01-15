GRIMOIRE_CONFIG = {
    "height": 278,
    "weidth": 509,
    "texture": "media/ui/Grimoire.png",

    "bookmark_textures": "media/ui/bookmarking/spr_book_section_makers_{}.png",
    "bookmark_count": 7,

    # отступы
    "padding": 50,
    "bookmark_height": 30,
    "bookmark_top_margin": 15,
    "arrow_size": 40,

}

GRIMOIRE_CHAPTER_1 = {
    "id" : "introduction",
    "title" : "Вступление, статы",
    "bookmark_index": 0,
    "locked": False, # изначально не заблокирована
    "pages": [
            {
                "id": "intro_1",
                "type": "text",
                "title": "Вступление",
                "content": "Гримуар алхимика. Основы магии.",
                "locked": False
            },
            {
                "id": "intro_2",
                "type": "text",
                "title": "Статы",
                "content": "Стрелки - перелистывание. Закладки - главы.",
                "locked": False
            }
        ]
}