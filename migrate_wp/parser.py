"""Parseur d'articles du site vitrine historique"""

import re
import unicodedata
from html import unescape
from html.parser import HTMLParser

from .importer import map_public_files
from ._special_content import portraits_anciens, adhesion_paypal

class MLStripper(HTMLParser):
    """Classe de retrait des tags HTML"""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.reset()
        self.fed = []

    def handle_data(self, data):
        """Gère une donnée"""
        self.fed.append(data)

    def handle_entityref(self, name):
        """Gère une référence d'entité"""
        self.fed.append('&%s;' % name)

    def handle_charref(self, name):
        """Gère une référence de caractère"""
        self.fed.append('&#%s;' % name)

    def get_data(self):
        """Récupère les données"""
        return ''.join(self.fed)

    def error(self, message):
        """Gère une erreur"""
        pass

def _strip_once(value):
    """Internal tag stripping utility used by strip_tags."""
    stripper = MLStripper()
    stripper.feed(value)
    stripper.close()
    return stripper.get_data()

def strip_tags(value):
    """Return the given HTML with all tags stripped."""
    # Note: in typical case this loop executes _strip_once once. Loop condition
    # is redundant, but helps to reduce number of executions of _strip_once.
    value = str(value)
    while '<' in value and '>' in value:
        new_value = _strip_once(value)
        if len(new_value) >= len(value):
            # _strip_once was not able to detect more tags
            break
        value = new_value
    return value

def make_title(title):
    """Retourne un titre sans formattage"""
    return strip_tags(title).strip()

def make_slug(title):
    """Retourne un slug d'article"""
    slug = re.sub(r"[dl]['’]|[\(\)]", r"", title.lower())
    slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r"\b(a|des?|du|et|les?|la)\b", r"", slug)
    slug = re.sub(r"[^a-z0-9]+", r"-", slug)
    slug = slug.strip('-')
    return slug

class Parser:
    """Parseur d'article"""
    def __init__(self, files):
        self.files = map_public_files(files)

    def print_image(self, match):
        """Retourne le code d'image correspondant à un fichier public"""
        if match.group(1) in self.files:
            file = self.files[match.group(1)]
            if file['type'] in ['jpg', 'png', 'gif', 'bmp']:
                out = "<div id=\"imageBlocGeneral\">\n"
                out += "<div id=\"imageBlocImage\">\n"
                out += "<img src=\"https://enet.ada-risques.fr/fichierPublic/"
                out += "{file[id]}.{file[type]}\">\n".format(file=file)
                out += "</div>\n"

                if match.group(2):
                    out += "<div id=\"imageBlocLegende\">\n<p>"
                    out += "{0}</p>\n</div>\n".format(match.group(2))

                out += "</div>\n"
                return out
            else:
                message = "Le fichier cible n'est pas une image !<br>"
                message += "Seuls les fichiers .jpg, les .png, les .gif et les .bmp sont autorisés"
                return message
        else:
            message = "<span style=\"color:red;font-weight:bold\"><u>/!\\</u>"
            message += "La référence de l'image est invalide : {0}</span>"
            print("Invalid file: {0}".format(match.group(1)))
            return message.format(match.group(1))

    def parse_text(self, bb_coded):
        """Parse du text BBCode et retourne son équivalent HTML"""
        text = bb_coded
        #    //$text = preg_replace("#\[img\]((ht|f)tp://)([^\r\n\t<\"]*?)\[/img\]#sie",
        #                           "'<img src=\\1' . str_replace(' ', '%20', '\\3') . '>'",
        #                           $text);
        #
        #    // Gestion des portraits d'anciens
        #        $text = preg_replace("/\[portraitsAnciens\]/", portraitsAnciens(), $text);
        text = text.replace("[portraitsAnciens]", portraits_anciens())
        #
        #    // Gestion des liens
        text = re.sub(r"\[url=([^\]]*)\]", r"<a href=\"\1\" target=\"_blank\">", text)
        text = re.sub(r"(?si)\[url=((?:ht|f)tps?://([^\r\n\t<\"\]]*))\]",
                      r"<a href=\"\1\" target=\"_blank\">", text)
        text = re.sub(r"\[urlinterne=([^\]]*)\]", r"<a href=\"\1\">", text)
        text = text.replace("[/url]", "</a>")
        #
        #    // Gestion des titres
        text = re.sub(r"\[(/?)t([1-6])\]", r"<\1h\2>", text)
        #
        #    //Gestion des tableaux
        #        $text = preg_replace_callback("#\[tab\](.*)\[\/tab\]#s",
        #                                      "tableauTextAreaV2",
        #                                      $text);
        #        // gardé pour la compatibilité avec l'ancienne version de traitement
        #        $text = preg_replace_callback("#\[tableau\](.*)\[\/tableau\]#s",
        #                                      "tableauTextArea",
        #                                      $text);
        text = re.sub(r"\[(/?)tableau\]", r"<\1table>", text)
        text = re.sub(r"\[(/?)l\]", r"<\1tr>", text)
        text = re.sub(r"\[(/?)c\]", r"<\1td>", text)
        #
        #    // Image avec ou sans légende
        text = re.sub(r"\[img=(\d+)\](?:([^\r\n\t<\"]*)\[\/img\])?", self.print_image, text)
        #
        #    // Gestion des liens pour les BI
        #        $text = preg_replace_callback("/\[BI=(\d+)\]/", "lienBI", $text);
        #    // Gestion des liens pour les fichiers publics
        #        $text = preg_replace_callback(
        #                   "/\[fichier=(\d+)\]([^\r\n\t<\"]*?)\[\/fichier\]/",
        #                   "lienFichierPublic",
        #                   $text);
        #
        text = re.sub(r"\[(/?)([biu])\]", r"<\1\2>", text)
        text = re.sub(r"\[(/?)g\]", r"<\1b>", text)
        text = re.sub(r"\[(/?)s\]", r"<\1u>", text)

        #    //$text = preg_replace("#\[centrer\]([^\x00\x08\x1F\x7F]+?)\[\/centrer\]#",
        #                           "<div align=\"center\">"
        #                               .str_replace("\r\n","<br>","$1")
        #                               ."</div>",
        #                           $text);
        text = re.sub(r"\[center\](.*[\r\n])\[/center\]",
                      r"<div align=\"center\">\1</div>", text)
        #    $text = preg_replace("#\[centrer\](.*[\r\n]*)\[\/centrer\]#",
        #                         "<div align=\"center\">$1</div>",
        #                         $text);
        text = text.replace('[centrer]', '<div style="text-align:center">')
        text = text.replace('[/centrer]', '</div>')
        #    //$text = str_replace("[centrer]","<div align=\"center\">",$text);
        #    //$text = str_replace("[/centrer]","</div>",$text);
        #
        text = re.sub(r"\[code\](.*)\[\/code\]",
                      r"\n<b>Code :</b>\n<div class=\"code\">\1</div>\n", text)
        text = re.sub(r"(?s)\[quote\](.*)\[\/quote\]",
                      r"\n<b>Quote :</b>\n<div class=\"quote\">\1</div>\n", text)
        text = re.sub(r"\[quote=(.*)\](.*)\[\/quote\]",
                      r"\n<b>Quote \1 :</b>\n<div class=\"quote\">\2</div>\n", text)
        text = re.sub(r"(?s)\[color=(.*)\](.*)\[\/color\]",
                      r"<span style=\"color:\1\">\2</span>", text)
        #TODO TODO TODO TODO TODO
        #    $text = preg_replace("#((^|\n|^ |\n )- )(.+)(\r|$)#",
        #                         "<ul><li>$3</li></ul>\n",
        #                         $text);
        text = re.sub(r"((^|\n|^ |\n )- )(.+)(\r|$)",
                      r"<ul>\n<li>\3</li>\n</ul>\n", text)
        text = text.replace("</ul>\n<ul>\n", "")
        #
        #    $text = preg_replace("/\[compositionCA\]/", compositionCA(), $text);
        #    $text = preg_replace("/\[compositionBureau\]/", compositionBureau(), $text);
        #
        #    $text = preg_replace("/\[adhesionPaypal\]/", adhesionPaypal(), $text);
        text = text.replace("[adhesionPaypal]", adhesion_paypal())
        #
        #    $text = preg_replace("/(^|\n)(.+)(\r|$)/", "<p class=\"paragraphe1\">$2</p>", $text);
        #
        text = text.replace("\r\n", "\n")
        text = unescape(text)

        return text
