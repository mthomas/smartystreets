import json
import pprint
import urllib

class Lookup():
    DPV_FOOTNOTE_LOOKUP = {
        "AA" : "City/state/zip + Street are all valid",
        "A1" : "ZIP+4 not matched; address is invalid (city/state/zip + street don't match)",
        "BB" : "ZIP+4 matched; Confirmed entire address; address is valid",
        "CC" : "Confirmed address by dropping secondary (apartment, suite, etc.) information",
        "F1" : "Matched to military address",
        "G1" : "Matched to general delivery address",
        "M1" : "Primary number (e.g. house number) is missing",
        "M3" : "Primary number (e.g. house number) is invalid",
        "N1" : "Confirmed with missing secondary information; address is valid but it also needs a secondary number (apartment, suite, etc.)",
        "P1" : "PO, RR, or HC box number is missing",
        "P3" : "PO, RR, or HC box number is invalid",
        "RR" : "Confirmed address with private mailbox (PMB) info",
        "R1" : "Confirmed address without private mailbox (PMB) info",
        "U1" : "Matched a unique ZIP code"
    }

    FOOTNOTE_LOOKUP = {
        "A": "Corrected ZIP code",
        "B": "Fixed city/state spelling",
        "C": "Invalid city/ state/ZIP",
        "D": "No ZIP+4 assigned",
        "E": "Same ZIP for multiple",
        "F": "Address not found",
        "G": "Used firm data",
        "H": "Missing secondary number",
        "I": "Insufficient/ incorrect address data",
        "J": "Dual address",
        "K": "Cardinal rule match",
        "L": "Changed address component",
        "LL": "Flagged address for LACSLink",
        "LI": "Flagged address for LACSLink",
        "M": "Fixed street spelling",
        "N": "Fixed abbreviations",
        "O": "Multiple ZIP+4; lowest used",
        "P": "Better address exists",
        "Q": "Unique ZIP match",
        "R": "No match; EWS: Match soon",
        "S": "Bad secondary address",
        "T": "Multiple response due to magnet street syndrome",
        "U": "Unofficial post office name",
        "V": "Unverifiable city / state",
        "W": "Invalid delivery address",
        "X": "Unique ZIP code",
        "Y": "Military match",
        "Z": "Matched with ZIPMOVE"
    }

    def __init__(self, auth_id, auth_token):
        self.auth_id = auth_id
        self.auth_token = auth_token

    def lookup(self, street, street2=None, city=None, state=None, zip_code=None, candidates=1):
        LOCATION = "https://api.smartystreets.com/street-address/"
        params = {   # entire query sting must be URL-Encoded
            "auth-id": self.auth_id,
            "auth-token": self.auth_token,
            "street": street,
            "street2": street2,
            "city": city,
            "state": state,
            "zipCode": zip_code,
            "candidates": str(candidates),
        }

        QUERY_STRING = urllib.urlencode({k:v for k,v in params.iteritems() if v is not None})

        URL = LOCATION + "?" + QUERY_STRING
        response = urllib.urlopen(URL).read()
        data = json.loads(response)
        
        for address in data:
            address["dpv_footnotes"] = {}    
            address["input_footnotes"] = {}

            footnotes = address["analysis"]["dpv_footnotes"]
            n = 2
            notes = [footnotes[i:i+n] for i in range(0, len(footnotes), n)]
            for note in notes:
                reason = self.DPV_FOOTNOTE_LOOKUP.get(note, "Unknown")
                address["dpv_footnotes"][note] = {"note": reason, "good": note[0] == note[1]}

            footnotes = address["analysis"]["footnotes"]
            notes=footnotes.split("#")
            for note in notes:
                if note != '':
                    reason = self.FOOTNOTE_LOOKUP.get(note, "Unknown")
                    address["input_footnotes"][note] = {"note": reason, "good": False}

        return data
