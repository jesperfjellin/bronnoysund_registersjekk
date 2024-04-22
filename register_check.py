import requests

def hent_enhet(orgnr):
    # Fjerner mellomrom fra organisasjonsnummeret og henter enhetsinformasjon.
    orgnr = orgnr.replace(" ", "")
    url = f'https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f'En feil oppstod under henting av data for {orgnr}: {e}')
        return None

def sjekk_status_og_skriver_informasjon(enhet_info, orgnr):
    # Sjekker status og skriver ut relevant informasjon om foretaket.
    navn = enhet_info.get('navn')
    registrert = enhet_info.get('registreringsdatoEnhetsregisteret')
    
    konkurs = enhet_info.get('konkurs', False)
    under_avvikling = enhet_info.get('underAvvikling', False)
    tvangsavvikling_eller_oppløsning = enhet_info.get('underTvangsavviklingEllerTvangsopplosning', False)

    if not konkurs and not under_avvikling and not tvangsavvikling_eller_oppløsning:
        print(f'Foretak {orgnr} {navn} er aktivt og operativt. Foretaket ble registrert i {registrert}.')
    else:
        status = []
        if konkurs:
            status.append('konkurs')
        if under_avvikling:
            status.append('under avvikling')
        if tvangsavvikling_eller_oppløsning:
            status.append('under tvangsavvikling eller tvangsoppløsning')
        print(f"Foretak {orgnr} {navn} er ikke aktivt. Status: {', '.join(status)}")

orgnumre = ['980489698']

for orgnr in orgnumre:
    enhet_info = hent_enhet(orgnr)
    if enhet_info:
        sjekk_status_og_skriver_informasjon(enhet_info, orgnr)
    else:
        print(f'Foretak {orgnr} eksisterer ikke i registeret, og kan ha blitt fusjonert eller slettet.')
