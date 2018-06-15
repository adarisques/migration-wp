"""Contenu spécifique"""

def _prenom_nom(pseudo, prenom, nom, promo, poste):
    """Retourne l'entrée de liste pour un portrait d'ancien"""
    lien = "    <li>"
    lien += "<a href=\"https://enet.ada-risques.fr/session/pages/index.php?"
    lien += "page_=../membres/membres&menu=info_membre&pseudo_voir={0}\">".format(pseudo)
    lien += "{0} {1}</a> ({2}) :".format(prenom, nom, promo)
    lien += " <a href=\"./profils/{0}.pdf\">{1}</a>".format(pseudo, poste)
    lien += "</li>\n"
    return lien

def portraits_anciens():
    """Retourne une liste de portraits d'anciens"""
    sortie = "<ul>\n"
    sortie += _prenom_nom("charlotte.barre", "Charlotte", "Barre", "2007 MRI",
                          "Sécurité chez Véolia Transport")
    sortie += _prenom_nom("julien.malfilatre", "Julien", "Malfilatre", "2007 STI",
                          "DBA Oracle")
    sortie += _prenom_nom("stephanie.fournier", "Stéphanie", "Fournier", "2007 MRI",
                          "Une expérience de VIE")
    sortie += _prenom_nom("vianney.besnard", "Vianney", "Besnard", "2002 MRI",
                          "Responsable Spécifications Techniques d'Exploitation EPR OLs")
    sortie += "</ul>\n"
    return sortie

def adhesion_paypal():
    """Retourne un formulaire PayPal"""
    retour = "<form action=\"https://www.paypal.com/cgi-bin/webscr\" method=\"post\" "
    retour += "target=\"_top\">\n"
    retour += "    <input type=\"hidden\" name=\"cmd\" value=\"_s-xclick\">\n"
    retour += "    <input type=\"hidden\" name=\"hosted_button_id\" value=\"PY8PVBC38XT6C\">\n"
    retour += "    <table>\n"
    retour += "        <tr><td>"
    retour += "<input type=\"hidden\" name=\"on0\" value=\"Cotisations :\">"
    retour += "Cotisations :</td></tr>\n"
    retour += "        <tr><td><select name=\"os0\">\n"
    retour += "                <option value=\"Adhésions AdA + INSA CVL Alumni\">"
    retour += "Adhésions AdA + INSA CVL Alumni 21,00 EUR</option>\n"
    retour += "                <option value=\"Adhésion complémentaire INSA CVL Alumni\">"
    retour += "Adhésion complémentaire INSA CVL Alumni 11,00 EUR</option>\n"
    retour += "                <option value=\"Adhésion AdA seule\">"
    retour += "Adhésion AdA seule 11,00 EUR</option>\n"
    retour += "                <option value=\"Adhésions + Don de soutien\">"
    retour += "Adhésions + Don de soutien 31,00 EUR</option>\n"
    retour += "                <option value=\"Adhésions + Don de soutien\">"
    retour += "Adhésions + Don de soutien 41,00 EUR</option>\n"
    retour += "        </select></td></tr>\n"
    retour += "        <tr><td>"
    retour += "<input type=\"hidden\" name=\"on1\" value=\"Nom, prénom, promo :\">"
    retour += "Nom, prénom, promo :"
    retour += "</td></tr>\n"
    retour += "        <tr><td><input type=\"text\" name=\"os1\" maxlength=\"200\"></td></tr>\n"
    retour += "        <tr><td><input type=\"hidden\" name=\"on2\" value=\"Mail :\">"
    retour += "Mail :</td></tr>\n"
    retour += "        <tr><td><input type=\"text\" name=\"os2\" maxlength=\"200\"></td></tr>\n"
    retour += "    </table>\n"
    retour += "    <input type=\"hidden\" name=\"currency_code\" value=\"EUR\">\n"
    retour += "    <input type=\"image\" "
    retour += "src=\"https://www.paypalobjects.com/fr_FR/FR/i/btn/btn_paynow_LG.gif\" "
    retour += "border=\"0\" name=\"submit\" "
    retour += "alt=\"PayPal, le réflexe sécurité pour payer en ligne\">\n"
    retour += "    <img alt=\"\" border=\"0\" "
    retour += "src=\"https://www.paypalobjects.com/fr_FR/i/scr/pixel.gif\" width=\"1\" "
    retour += "height=\"1\">\n"
    retour += "</form>\n"
    return retour
