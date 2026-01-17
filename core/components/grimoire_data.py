GRIMOIRE_CONFIG = {
    "height": 278,
    "width": 509,
    "texture": "media/ui/Grimoire.png",

    "bookmark_textures": "media/ui/bookmarking/spr_book_section_makers_{}.png",

    "left_arrow_texture": "media/ui/spr_book_turn_pages/spr_book_turn_pages_0.png",
    "right_arrow_texture": "media/ui/spr_book_turn_pages/spr_book_turn_pages_2.png",
    "bookmark_count": 7,

    # отступы
    "padding": 50,
    "bookmark_height": 30,
    "bookmark_top_margin": 15,
    "arrow_size": 40,
    "font_size": 14,
}
GRIMOIRE_TEXT_MARGINS = {
    "left_page": {
        "x": 60,  # отступ от левого края
        "y": 30,  # отступ сверху
        "width": 170,
        "height": 205
    },
    "right_page": {
        "x": 270,  # отступ от левого края
        "y": 30,  # отступ сверху
        "width": 170,
        "height": 205
    }
}

GRIMOIRE_CHAPTER_1 = {
    "id": "introduction",
    "bookmark_index": 0,
    "locked": False,  # изначально не заблокирована

}
GRIMOIRE_CHAPTER_1_PAGES = [
    # страница индексом 0
    {
        "id": "intro_0",
        "type": "text",
        "content": "страница 1 текст текст",
        "locked": False
    },
    # страница индексом 1
    {
        "id": "intro_1",
        "type": "text",
        "content": "страница 2 текст текст",
        "locked": False
    },
    # страница индексом 2 - фактически 3 страница
    {
        "id": "intro_2",
        "type": "text",
        "content": "страница 3 текст текст текст",
        "locked": False
    }
]
