import click

from ham_t.commands import get_site, pass_context
from ham_t.exceptions import SiteNotSpecifiedError


# translation
@click.command("build-message-files")
@pass_context
def build_message_files(context):
	"Build message files for translation"
	import ham_t.translate

	for site in context.sites:
		try:
			ham_t.init(site=site)
			ham_t.connect()
			ham_t.translate.rebuild_all_translation_files()
		finally:
			ham_t.destroy()
	if not context.sites:
		raise SiteNotSpecifiedError


@click.command("new-language")  # , help="Create lang-code.csv for given app")
@pass_context
@click.argument("lang_code")  # , help="Language code eg. en")
@click.argument("app")  # , help="App name eg. ham_t")
def new_language(context, lang_code, app):
	"""Create lang-code.csv for given app"""
	import ham_t.translate

	if not context["sites"]:
		raise Exception("--site is required")

	# init site
	ham_t.connect(site=context["sites"][0])
	ham_t.translate.write_translations_file(app, lang_code)

	print(
		"File created at ./apps/{app}/{app}/translations/{lang_code}.csv".format(
			app=app, lang_code=lang_code
		)
	)
	print(
		"You will need to add the language in ham_t/geo/languages.json, if you haven't done it already."
	)


@click.command("get-untranslated")
@click.option("--app", default="_ALL_APPS")
@click.argument("lang")
@click.argument("untranslated_file")
@click.option("--all", default=False, is_flag=True, help="Get all message strings")
@pass_context
def get_untranslated(context, lang, untranslated_file, app="_ALL_APPS", all=None):
	"Get untranslated strings for language"
	import ham_t.translate

	site = get_site(context)
	try:
		ham_t.init(site=site)
		ham_t.connect()
		ham_t.translate.get_untranslated(lang, untranslated_file, get_all=all, app=app)
	finally:
		ham_t.destroy()


@click.command("update-translations")
@click.option("--app", default="_ALL_APPS")
@click.argument("lang")
@click.argument("untranslated_file")
@click.argument("translated-file")
@pass_context
def update_translations(context, lang, untranslated_file, translated_file, app="_ALL_APPS"):
	"Update translated strings"
	import ham_t.translate

	site = get_site(context)
	try:
		ham_t.init(site=site)
		ham_t.connect()
		ham_t.translate.update_translations(lang, untranslated_file, translated_file, app=app)
	finally:
		ham_t.destroy()


@click.command("import-translations")
@click.argument("lang")
@click.argument("path")
@pass_context
def import_translations(context, lang, path):
	"Update translated strings"
	import ham_t.translate

	site = get_site(context)
	try:
		ham_t.init(site=site)
		ham_t.connect()
		ham_t.translate.import_translations(lang, path)
	finally:
		ham_t.destroy()


commands = [
	build_message_files,
	get_untranslated,
	import_translations,
	new_language,
	update_translations,
]
