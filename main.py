import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

BOT_TOKEN = "8751607847:AAESpx7VsCRJJyjeAP4Rg36_tPdxypxKEIo"
WHATSAPP_NUMBER = "56961764267"
EMAIL = "contacto@etsjayim.cl"
WEBSITE = "https://www.etsjayim.cl"
RABINO = "Rabino Israel Escalona"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WELCOME = """
🕍 *עץ חיים — ETZ JAYIM*
_Árbol de Vida · Beit Hakneset_

*Bienvenido/a*

Soy el asistente de estudio de la comunidad Etz Jayim, bajo la dirección del *Rabino Israel Escalona*.

¿Qué deseas explorar hoy?

_כִּי עֵץ חַיִּים הִיא לַמַּחֲזִיקִים בָּהּ_
_Árbol de vida es para quienes la sostienen — Prov. 3:18_
"""

CONTACT_TEXT = """
👤 *HABLAR CON ALGUIEN*
_Beit Hakneset Etz Jayim_

Estamos aquí. Cada pregunta merece una respuesta honesta y sin presión.

🕍 *Rabino Israel Escalona*
Comunidad Mesiánica — Chile

💬 *WhatsApp:* +56961764267
✉️ *Email:* contacto@etsjayim.cl
🌐 *Web:* www.etsjayim.cl
"""

TEXTS = {
    "mesianico": {"title": "✡️ ¿Qué es ser mesiánico?", "text": "Un creyente *mesiánico* es alguien que acepta a *Yeshua HaMashiaj* como el cumplimiento de las profecías de la Torah — y que abraza la herencia judía de la Biblia.\n\nNo es solo cristiano ni solo judío: es el *camino más antiguo y original* de los primeros seguidores de Yeshua — que eran todos judíos."},
    "mesianico_historia": {"title": "🏛️ Historia del movimiento mesiánico", "text": "Los primeros seguidores de Yeshua eran *judíos observantes* que no dejaron de guardar el Shabbat, las fiestas ni la Torah.\n\nCon el tiempo, la helenización separó la fe de sus raíces hebreas. En el siglo XX el movimiento mesiánico *retornó a sus orígenes*."},
    "mesianico_diferencia": {"title": "⚖️ Diferencias con el cristianismo", "text": "El judaísmo mesiánico *no reemplaza la Torah con la gracia* — las integra.\n\nYeshua mismo dijo:\n_'No penséis que vine a abolir la Torah'_ (Mateo 5:17)"},
    "mesianico_practica": {"title": "🕯️ La vida mesiánica en la práctica", "text": "El creyente mesiánico estructura su semana en torno al *Shabbat*, celebra las fiestas del calendario hebreo, estudia Torah y ora con las plegarias tradicionales judías.\n\nNo es una lista de obligaciones — es un *camino de vida*."},
    "torah": {"title": "📜 ¿Qué es la Torah?", "text": "La Torah no significa 'ley' — significa *'instrucción', 'enseñanza'*.\n\nEs la revelación que Dios entregó a Moshé en el Sinaí: los cinco libros de Moshé, más la Torah Oral que los explica.\n\nPara el creyente mesiánico, la Torah es el *fundamento eterno* sobre el que Yeshua construyó."},
    "torah_escrita": {"title": "📖 Torah Escrita y Torah Oral", "text": "En el Sinaí, Dios entregó dos dimensiones:\n\n📖 *Torah Escrita* — los cinco libros\n🗣️ *Torah Oral* — su explicación detallada, documentada en el Talmud\n\nSin la Torah Oral, la Torah Escrita es incompleta."},
    "torah_613": {"title": "⚖️ Los 613 mandamientos", "text": "El Rambam contó *613 mitzvot* en la Torah:\n• 248 positivos\n• 365 negativos\n\nPara el creyente no judío mesiánico, el punto de partida son las *Siete Leyes de Noaj*, con crecimiento progresivo."},
    "torah_yeshua": {"title": "⭐ Yeshua y la Torah", "text": "Mateo 5:17:\n_'No penséis que vine a abolir la Torah; no vine a abolir sino a *cumplir*.'_\n\nYeshua vivió como maestro judío del siglo I debatiendo la Halajá — no contra ella. *Más Torah, no menos.*"},
    "fiestas": {"title": "🕯️ Las fiestas judías", "text": "Las fiestas del calendario hebreo no son tradiciones culturales — son *citas divinas* (Moadim).\n\nDios las llama _'Mis fiestas señaladas'_ (Vayikrá 23).\n\nPara el creyente mesiánico, cada fiesta es una profecía *cumplida o por cumplir* en Yeshua."},
    "fiestas_pesaj": {"title": "🍷 Pésaj — La Pascua", "text": "Pésaj conmemora la liberación de Egipto.\n\nYeshua celebró su última cena *como un Seder de Pésaj*.\n\nPablo declara:\n_'Nuestra Pascua, que es Yeshua, ya fue sacrificada'_ (1 Cor. 5:7)\n\nPésaj no terminó — se *profundizó*."},
    "fiestas_shavuot": {"title": "📜 Shavuot — Pentecostés", "text": "Shavuot celebra la entrega de la Torah en el Sinaí.\n\nEn este mismo día — según Hechos 2 — el *Ruaj HaKodesh* fue derramado sobre los discípulos.\n\n*El mismo día. La misma fiesta. Una profundidad mayor.*"},
    "fiestas_roshhashana": {"title": "🎺 Rosh Hashaná — Año Nuevo", "text": "El día del *Shofar* y del Juicio celestial.\n\nEl sonido del Shofar anuncia el Día del Señor y la resurrección final (1 Tes. 4:16).\n\nPara el creyente mesiánico, Rosh Hashaná es un *ensayo anual del encuentro final* con el Eterno."},
    "fiestas_yomkipur": {"title": "🕊️ Yom Kipur — Día de Expiación", "text": "El día más sagrado del año judío. Ayuno de 25 horas y *Teshuvá* — retorno a Dios.\n\nEs el día de la *renovación del alma*, del perdón honesto, del regreso radical a lo que uno realmente es."},
    "fiestas_sucot": {"title": "🌿 Sucot — Tabernáculos", "text": "La fiesta más universal de todas.\n\nZacarías 14:16 profetiza que *todas las naciones* celebrarán Sucot en la era mesiánica.\n\nJuan 1:14: Yeshua *'plantó su Sucá entre nosotros'*."},
    "yeshua": {"title": "⭐ ¿Quién es Yeshua?", "text": "*Yeshua* (ישוע) es el nombre hebreo de Jesús.\n\nNació en Israel, vivió como judío observante del siglo I, enseñó Torah con autoridad extraordinaria y fue reconocido como el *HaMashiaj* — el Ungido profetizado por los profetas de Israel."},
    "yeshua_judio": {"title": "✡️ Yeshua el judío", "text": "Yeshua fue circuncidado, presentado en el Templo, celebró Pésaj, Shavuot, Sucot y Janucá. Enseñó en sinagogas. Usó Tzitzit. Debatió Halajá.\n\nEl erudito judío *David Flusser* documentó que Yeshua es *incomprensible fuera del judaísmo* del Segundo Templo."},
    "yeshua_profecia": {"title": "📜 Las profecías mesiánicas", "text": "La Tanaj contiene más de 300 referencias al Mashiaj:\n\n📖 *Isaías 53* — el Siervo sufriente\n📍 *Miqueas 5:1* — nacerá en Belén\n💔 *Zacarías 12:10* — 'mirarán a Aquel a quien traspasaron'"},
    "cabala": {"title": "🌳 ¿Qué es la Cábala?", "text": "La *Cábala* es la dimensión mística del judaísmo: el estudio de la estructura espiritual de la realidad, los mundos invisibles y el alma humana.\n\nNo es magia — es _la ciencia espiritual más antigua de Occidente_."},
    "cabala_sefirot": {"title": "🌳 Las Sefirot", "text": "Las *diez Sefirot* son los canales a través de los cuales Dios gobierna la realidad:\n\n_Keter · Jojmah · Binah · Jesed · Guevurah · Tiferet · Netzaj · Hod · Yesod · Maljut_\n\nComo los colores del espectro que emergen de *una única luz blanca*."},
    "cabala_alma": {"title": "✨ Los cinco niveles del alma", "text": "🔴 *Nefesh* — alma vital\n🟠 *Ruaj* — alma emocional\n🟡 *Neshamah* — alma intelectual\n🟢 *Jayah* — alma de la voluntad\n⚪ *Yejidah* — chispa de unidad con Dios\n\nEl hombre habita todos los niveles simultáneamente."},
    "shabbat": {"title": "🕍 ¿Qué es el Shabbat?", "text": "El Shabbat es el séptimo día — del atardecer del viernes a la noche del sábado.\n\nNo es solo descanso físico: es un *acto sagrado semanal*.\n\n_'El Shabbat fue hecho para el hombre'_ (Marcos 2:27)"},
    "shabbat_como": {"title": "🕯️ Cómo observar el Shabbat", "text": "🕯️ *Viernes al atardecer:* Encender dos velas. Kidush sobre el vino. Mesa especial con Jalá.\n\n🤫 *Durante el Shabbat:* Descanso, familia, Torah, comunidad.\n\n✨ *Al cierre:* Havdalá — separación entre lo sagrado y lo ordinario."},
    "shabbat_yeshua": {"title": "⭐ Yeshua y el Shabbat", "text": "Yeshua sanó en Shabbat para revelar su propósito más profundo: es el día de la *restauración y la liberación*.\n\n_'El Señor del Shabbat'_ no lo abolió — lo *cumplió en plenitud*."},
    "paranosotros": {"title": "💫 ¿Esto es para mí?", "text": "✡️ *¿Eres judío?* Este camino es el retorno a tus raíces más profundas.\n\n🌍 *¿No eres judío?* La Torah siempre tuvo una puerta para las naciones — y Yeshua la abrió de par en par.\n\nNo hay que 'ser judío de nacimiento'. Hay que tener el *corazón dispuesto*."},
    "oracion": {"title": "🙏 ¿Cómo orar como judío?", "text": "La plegaria judía es *Halajá* — mandamiento estructurado con tiempos y formas.\n\n🌅 *Shajarit* — mañana\n🌤️ *Minjá* — tarde\n🌙 *Arvit* — noche\n\nEl Padrenuestro que Yeshua enseñó es una *síntesis magistral* de la Amidá judía."},
    "oracion_shema": {"title": "📜 El Shemá", "text": "_'Escucha, Israel, el Eterno es nuestro Dios, el Eterno es Uno.'_ (Devarim 6:4)\n\nEl Shemá se recita *mañana y noche*. Yeshua lo citó como el primer mandamiento (Marcos 12:29).\n\n*Todo es Uno. Solo hay Una Realidad. Y esa Realidad es personal.*"},
    "oracion_padrenuestro": {"title": "🙏 El Padrenuestro como Tefila judía", "text": "Cada línea del Padrenuestro tiene paralelo en la Amidá judía:\n\n📌 _'Santificado sea Tu Nombre'_ → Kedushah\n👑 _'Venga Tu Reino'_ → Maljuyot\n🙏 _'Perdona nuestras deudas'_ → Selijá\n\nYeshua entregó la *esencia de lo que ya existía*."},
    "comunidad": {"title": "🏠 ¿Cómo unirme?", "text": "*Beit Hakneset Etz Jayim* es una comunidad mesiánica en Chile, bajo la dirección del *Rabino Israel Escalona*.\n\nRecibimos a personas de todas las trayectorias.\n\nEl primer paso es simple: *presentarte*. Sin compromisos. Sin presión."},
    "cursos": {"title": "📚 Cursos de Etz Jayim", "text": "🌳 *Mística Judía Aplicada*\n15 clases + Bonus Track\n\n📜 *Halajá Esencial Mesiánica*\n10 clases en 3 módulos + Bonus Track\n\n¿Cuál te interesa?"},
    "cursos_mistica": {"title": "🌳 Mística Judía Aplicada", "text": "*15 clases en 5 módulos + Bonus Track*\n\n📗 Módulo 1: Fundamentos de la Autoridad\n📘 Módulo 2: La Arquitectura Celestial\n📙 Módulo 3: Herramientas de Edición\n📕 Módulo 4: Aplicación Avanzada\n📔 Módulo 5: Responsabilidad y Madurez\n⭐ Bonus: Ein Sof y la Tzimtzum"},
    "cursos_halaja": {"title": "📜 Halajá Esencial Mesiánica", "text": "*10 clases en 3 módulos + Bonus Track*\n\n📗 Módulo 1: ¿Qué es la Halajá?\n📘 Módulo 2: Los Pilares\n📙 Módulo 3: Halajá Vivida\n⭐ Bonus: Na'ase VeNishma — El Sinaí Revisitado"},
}

def kb_single(buttons):
    rows = [[InlineKeyboardButton(b[0], callback_data=b[1])] for b in buttons]
    return InlineKeyboardMarkup(rows)

KEYBOARDS = {
    "home": kb_single([("✡️ ¿Qué es ser mesiánico?", "mesianico"), ("📜 ¿Qué es la Torah?", "torah"), ("🕯️ ¿Qué son las fiestas judías?", "fiestas"), ("⭐ ¿Quién es Yeshua?", "yeshua"), ("🌳 ¿Qué es la Cábala?", "cabala"), ("🕍 ¿Qué es el Shabbat?", "shabbat"), ("💫 ¿Esto es para mí?", "paranosotros"), ("🙏 ¿Cómo orar como judío?", "oracion"), ("🏠 ¿Cómo unirme a la comunidad?", "comunidad"), ("📚 ¿Qué cursos tienen?", "cursos")]),
    "mesianico": kb_single([("🏛️ Su historia", "mesianico_historia"), ("⚖️ Diferencias con el cristianismo", "mesianico_diferencia"), ("🕯️ Cómo se vive en la práctica", "mesianico_practica"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "mesianico_historia": kb_single([("↩ Volver", "mesianico"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "mesianico_diferencia": kb_single([("↩ Volver", "mesianico"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "mesianico_practica": kb_single([("🕍 Aprender sobre el Shabbat", "shabbat"), ("🕯️ Explorar las fiestas", "fiestas"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "torah": kb_single([("📖 Torah Escrita y Torah Oral", "torah_escrita"), ("⚖️ Los 613 mandamientos", "torah_613"), ("⭐ Yeshua y la Torah", "torah_yeshua"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "torah_escrita": kb_single([("↩ Volver", "torah"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "torah_613": kb_single([("↩ Volver", "torah"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "torah_yeshua": kb_single([("↩ Volver", "torah"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas": kb_single([("🍷 Pésaj", "fiestas_pesaj"), ("📜 Shavuot", "fiestas_shavuot"), ("🎺 Rosh Hashaná", "fiestas_roshhashana"), ("🕊️ Yom Kipur", "fiestas_yomkipur"), ("🌿 Sucot", "fiestas_sucot"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas_pesaj": kb_single([("↩ Volver", "fiestas"), ("👤 Quiero celebrar Pésaj", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas_shavuot": kb_single([("↩ Volver", "fiestas"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas_roshhashana": kb_single([("↩ Volver", "fiestas"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas_yomkipur": kb_single([("↩ Volver", "fiestas"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "fiestas_sucot": kb_single([("↩ Volver", "fiestas"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "yeshua": kb_single([("✡️ Yeshua el judío", "yeshua_judio"), ("📜 Las profecías mesiánicas", "yeshua_profecia"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "yeshua_judio": kb_single([("↩ Volver", "yeshua"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "yeshua_profecia": kb_single([("↩ Volver", "yeshua"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "cabala": kb_single([("🌳 Las Sefirot", "cabala_sefirot"), ("✨ Los cinco niveles del alma", "cabala_alma"), ("📚 Ver curso de Mística Judía", "cursos_mistica"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "cabala_sefirot": kb_single([("↩ Volver", "cabala"), ("👤 Quiero estudiar en profundidad", "contacto"), ("🏠 Inicio", "home")]),
    "cabala_alma": kb_single([("↩ Volver", "cabala"), ("👤 Quiero estudiar en profundidad", "contacto"), ("🏠 Inicio", "home")]),
    "shabbat": kb_single([("🕯️ ¿Cómo se observa?", "shabbat_como"), ("⭐ Yeshua y el Shabbat", "shabbat_yeshua"), ("👤 Quiero celebrar mi primer Shabbat", "contacto"), ("🏠 Inicio", "home")]),
    "shabbat_como": kb_single([("↩ Volver", "shabbat"), ("👤 Quiero aprender más", "contacto"), ("🏠 Inicio", "home")]),
    "shabbat_yeshua": kb_single([("↩ Volver", "shabbat"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "paranosotros": kb_single([("✡️ Soy judío y quiero explorar", "contacto"), ("🌍 No soy judío y me interesa", "contacto"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "oracion": kb_single([("📜 El Shemá", "oracion_shema"), ("🙏 El Padrenuestro como Tefila judía", "oracion_padrenuestro"), ("👤 Quiero aprender a orar", "contacto"), ("🏠 Inicio", "home")]),
    "oracion_shema": kb_single([("↩ Volver", "oracion"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "oracion_padrenuestro": kb_single([("↩ Volver", "oracion"), ("👤 Quiero hablar con alguien", "contacto"), ("🏠 Inicio", "home")]),
    "comunidad": kb_single([("💬 Contactar a la comunidad", "contacto"), ("📚 Ver los cursos", "cursos"), ("🏠 Inicio", "home")]),
    "cursos": kb_single([("🌳 Mística Judía Aplicada", "cursos_mistica"), ("📜 Halajá Esencial Mesiánica", "cursos_halaja"), ("👤 Quiero inscribirme", "contacto"), ("🏠 Inicio", "home")]),
    "cursos_mistica": kb_single([("↩ Volver", "cursos"), ("👤 Quiero inscribirme", "contacto"), ("🏠 Inicio", "home")]),
    "cursos_halaja": kb_single([("↩ Volver", "cursos"), ("👤 Quiero inscribirme", "contacto"), ("🏠 Inicio", "home")]),
    "contacto": kb_single([("🏠 Volver al inicio", "home")]),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode='Markdown', reply_markup=KEYBOARDS["home"])

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 *Menú Principal — Etz Jayim*\n\n¿Qué deseas explorar?", parse_mode='Markdown', reply_markup=KEYBOARDS["home"])

async def contacto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTACT_TEXT, parse_mode='Markdown', reply_markup=KEYBOARDS["contacto"])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "home":
        text = WELCOME
        kb_markup = KEYBOARDS["home"]
    elif data == "contacto":
        text = CONTACT_TEXT
        kb_markup = KEYBOARDS["contacto"]
    elif data in TEXTS:
        t = TEXTS[data]
        text = f"*{t['title']}*\n\n{t['text']}"
        kb_markup = KEYBOARDS.get(data, KEYBOARDS["home"])
    else:
        text = WELCOME
        kb_markup = KEYBOARDS["home"]
    try:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=kb_markup)
    except Exception:
        await query.message.reply_text(text, parse_mode='Markdown', reply_markup=kb_markup)

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕍 Usa los botones para navegar, o escribe:\n/menu — Menú principal\n/contacto — Contactar", parse_mode='Markdown', reply_markup=KEYBOARDS["home"])

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("contacto", contacto_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
    print("🕍 Bot Etz Jayim iniciado...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
