import requests

# --- DÉFINITION DES COULEURS ANSI ---
# Vous pouvez les adapter si vous utilisez un module de couleurs spécifique
red = '\033[91m' # Rouge Vif
white = '\033[97m' # Blanc Vif
reset = '\033[0m' # Réinitialiser la couleur/le format
# Définition des variables utilitaires manquantes
INFO_ADD = "" # Un simple emoji ou symbole
BEFORE = "" # Définissez ou retirez les variables d'heure/formatage d'input
AFTER = ""
INPUT = ">"

# Les fonctions et variables non standard (comme Title, Slow, ErrorModule, Error, ErrorUrl, etc.)
# sont conservées mais doivent être définies ailleurs dans votre code pour fonctionner.

try:
    # L'import doit être en dehors du bloc 'except Exception as e:'
    # La structure initiale 'import requests except Exception as e: ErrorModule(e)' n'est pas valide.
    pass # Rien à faire ici, l'import est déjà fait.
except Exception as e:
    # Ceci est juste pour capturer les erreurs de l'environnement si vous voulez garder cette structure.
    # En pratique, l'importation devrait être la première ligne.
    # ErrorModule(e) 
    pass # Retiré si ErrorModule n'est pas définie.

# Title("Discord Server Info") # Retiré/commenté si Title n'est pas définie.

try:
    # Slow(discord_banner) # Retiré/commenté si Slow/discord_banner ne sont pas définies.
    
    # Assurez-vous que les variables de formatage (BEFORE, AFTER, INPUT, reset, current_time_hour) sont définies
    # invite = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Server Invitation -> {reset}")
    invite = input(f"Entrez l'invitation au serveur Discord -> ") # Version simplifiée
    
    try:
        # Tente de récupérer le code d'invitation après le dernier '/'
        invite_code = invite.split("/")[-1]
    except Exception:
        # Si split échoue (par exemple, si 'invite' n'est pas une chaîne), utilise l'entrée brute
        invite_code = invite

    # L'API Discord pour les invitations est stable.
    response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")

    if response.status_code == 200:
        api = response.json()

        # --- Extraction des informations ---
        
        type_value = api.get('type', "None")
        code_value = api.get('code', "None")
        expires_at = api.get('expires_at', "None")
        flags = api.get('flags', "None")
        
        # Inviter Info
        inviter_info = api.get('inviter', {})
        inviter_id = inviter_info.get('id', "None")
        inviter_username = inviter_info.get('username', "None")
        inviter_avatar = inviter_info.get('avatar', "None")
        inviter_discriminator = inviter_info.get('discriminator', "None")
        inviter_public_flags = inviter_info.get('public_flags', "None")
        inviter_flags = inviter_info.get('flags', "None")
        inviter_banner = inviter_info.get('banner', "None")
        inviter_accent_color = inviter_info.get('accent_color', "None")
        inviter_global_name = inviter_info.get('global_name', "None")
        inviter_banner_color = inviter_info.get('banner_color', "None")
        
        # Server Info (Guild)
        server_info = api.get('guild', {})
        server_id = server_info.get('id', "None")
        server_name = server_info.get('name', "None")
        server_icon = server_info.get('icon', "None")
        server_features = server_info.get('features', "None")
        
        # Correction de la faute de frappe : 'server_descritpion' -> 'server_description'
        server_description = server_info.get('description', "None")
        
        server_verification_level = server_info.get('verification_level', "None")
        server_nsfw_level = server_info.get('nsfw_level', "None")
        server_nsfw = server_info.get('nsfw', "None")
        server_premium_subscription_count = server_info.get('premium_subscription_count', "None")
        
        # Formatage des features
        if isinstance(server_features, list): # Vérifie si c'est une liste avant de joindre
            server_features = ' / '.join(server_features)
        
        # Channel Info
        channel_info = api.get('channel', {})
        channel_id = channel_info.get('id', "None")
        channel_type = channel_info.get('type', "None")
        channel_name = channel_info.get('name', "None")
        
        # --- Affichage des informations (en supposant que red, white, INFO_ADD, Slow existent) ---
        
        # Slow(f""" ... """) # Le bloc Slow englobe l'affichage complet
        # Remplacez {server_descritpion} par {server_description}
        
        output_invitation = f"""
{red}Invitation Information:{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
  {INFO_ADD} Invitation                 : {white}{invite}{red}{reset}
  {INFO_ADD} Type                       : {white}{type_value}{red}{reset}
  {INFO_ADD} Code                       : {white}{code_value}{red}{reset}
  {INFO_ADD} Expired                    : {white}{expires_at}{red}{reset}
  {INFO_ADD} Server ID                  : {white}{server_id}{red}{reset}
  {INFO_ADD} Server Name                : {white}{server_name}{red}{reset}
  {INFO_ADD} Channel ID                 : {white}{channel_id}{red}{reset}
  {INFO_ADD} Channel Name               : {white}{channel_name}{red}{reset}
  {INFO_ADD} Channel Type               : {white}{channel_type}{red}{reset}
  {INFO_ADD} Server Description         : {white}{server_description}{red}{reset}
  {INFO_ADD} Server Icon                : {white}{server_icon}{red}{reset}
  {INFO_ADD} Server Features            : {white}{server_features}{red}{reset}
  {INFO_ADD} Server NSFW Level          : {white}{server_nsfw_level}{red}{reset}
  {INFO_ADD} Server NSFW                : {white}{server_nsfw}{red}{reset}
  {INFO_ADD} Flags                      : {white}{flags}{red}{reset}
  {INFO_ADD} Server Verification Level  : {white}{server_verification_level}{red}{reset}
  {INFO_ADD} Server Premium Subscription Count : {white}{server_premium_subscription_count}{red}{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
"""
        try:
            Slow(output_invitation)
        except NameError:
            print(output_invitation) # Utilisation de print si Slow n'est pas définie
            
        if inviter_info:
            output_inviter = f"""{red}Inviter Information:{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
  {INFO_ADD} ID                         : {white}{inviter_id}{red}{reset}
  {INFO_ADD} Username                   : {white}{inviter_username}{red}{reset}
  {INFO_ADD} Global Name                : {white}{inviter_global_name}{red}{reset}
  {INFO_ADD} Avatar                     : {white}{inviter_avatar}{red}{reset}
  {INFO_ADD} Discriminator              : {white}{inviter_discriminator}{red}{reset}
  {INFO_ADD} Public Flags               : {white}{inviter_public_flags}{red}{reset}
  {INFO_ADD} Flags                      : {white}{inviter_flags}{red}{reset}
  {INFO_ADD} Banner                     : {white}{inviter_banner}{red}{reset}
  {INFO_ADD} Accent Color               : {white}{inviter_accent_color}{red}{reset}
  {INFO_ADD} Banner Color               : {white}{inviter_banner_color}{red}{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
"""
            try:
                Slow(output_inviter)
            except NameError:
                print(output_inviter) # Utilisation de print si Slow n'est pas définie
            
    else:
        # ErrorUrl() # Retiré/commenté si ErrorUrl n'est pas définie.
        print("Erreur: Impossible de récupérer les informations de l'invitation (code de statut:", response.status_code, ")")
        
    # Continue() # Retiré/commenté si Continue n'est pas définie.
    # Reset() # Retiré/commenté si Reset n'est pas définie.
    
except requests.exceptions.RequestException as req_e:
    # Gestion spécifique des erreurs de requêtes (connexion, timeout, etc.)
    # Error(req_e) # Retiré/commenté si Error n'est pas définie.
    print(f"Erreur de requête: {req_e}")
except Exception as e:
    # Gestion des autres erreurs (e.g., JSON decoding, undefined variables if not caught)
    # Error(e) # Retiré/commenté si Error n'est pas définie.
    print(f"Une erreur inattendue est survenue: {e}")