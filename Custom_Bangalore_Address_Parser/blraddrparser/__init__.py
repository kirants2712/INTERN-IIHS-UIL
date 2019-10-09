#!/usr/bin/python
# -*- coding: utf-8 -*-

##
## Adapted from https://github.com/datamade/usaddress
##  for parsing Indian addresses, specifically for Bengaluru

from __future__ import print_function
from builtins import zip
from builtins import str
import os
import string
import re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import warnings

import pycrfsuite
import probableparsing

LABELS = [
    'PlotNumber',
    'BuildingName',
    'FloorNumber',
    'DoorNumber',
    'Level1StreetName',
    'Level2StreetName',
    'Landmark',
    'Neighbourhood',
    'Area',
    'City',
    'PIN',
    'District',
    'State',
    'Country'
    'Other'
    ]

MODEL_FILE = 'blraddr.crfsuite'
MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE

DIRECTIONS = set(['n', 's', 'e', 'w',
                  'ne', 'nw', 'se', 'sw',
                  'north', 'south', 'east', 'west',
                  'northeast', 'northwest', 'southeast', 'southwest'])

BUILDING_NAMES = {
        'building', 'bldg', 'bldng', 'tower', 'towers', 'manor', 'complex',
        'mall', 'apartment', 'apartments', 'plaza', 'arcade', 'school', 'college',
        'academy', 'factory', 'institute', 'station', 'hospital', 'clinic', 'hotel',
        'restaurant', 'shop', 'bank'
}

LANDMARK_NAMES = {
        'near', 'nr', 'opp', 'opposite', 'across', 'next', 'above', 'below'
}

STREET_NAMES = {
    'circle', 'cross', 'cr', 'crs', 'main', 'mainroad', 'mainrd', 'mn', 'road',
    'rd', 'street', 'st', 'highway', 'highwy', 'junction', 'junctn', 'lane', 'flyover'
}

LOCALITY_NAMES = {
    'phase', 'ph', 'sector', 'sec', 'sctr', 'stage', 'layout', 'nagar',
    'nagara', 'puram', 'pura', 'pet', 'pete', 'campus', 'area', 'halli',
    'angadi', 'slum', 'colony', 'lake', 'kere', 'market', 'town', 'hobli',
    'post', 'block', 'blk'
}

CITY_NAMES = {
    'blr', 'bengaluru', 'bangalore', 'bangalor', 'bengluru', 'bengalooru'
}

STATE_NAMES = {
    'karnataka'
}

PARENT_LABEL = 'AddressString'
GROUP_LABEL = 'AddressCollection'

try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(MODEL_PATH)
except IOError:
    warnings.warn('You must train the model (parserator train --trainfile '
                  'FILES) to create the %s file before you can use the parse '
                  'and tag methods' % MODEL_FILE)


def parse(address_string):
    tokens = tokenize(address_string)

    if not tokens:
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))


def tag(address_string, tag_mapping=None):
    tagged_address = OrderedDict()

    last_label = None
    is_intersection = False
    og_labels = []

    for token, label in parse(address_string):
        # saving old label
        og_labels.append(label)
        # map tag to a new tag if tag mapping is provided
        if tag_mapping and tag_mapping.get(label):
            label = tag_mapping.get(label)
        else:
            label = label

        if label == last_label:
            tagged_address[label].append(token)
        elif label not in tagged_address:
            tagged_address[label] = [token]
        else:
            raise RepeatedLabelError(address_string, parse(address_string),
                                     label)

        last_label = label

    for token in tagged_address:
        component = ' '.join(tagged_address[token])
        component = component.strip(" ,;")
        tagged_address[token] = component

    address_type = 'Street Address'

    return tagged_address, address_type


def tokenize(address_string):
    if isinstance(address_string, bytes):
        address_string = str(address_string, encoding='utf-8')
    address_string = re.sub('(&#38;)|(&amp;)', '&', address_string)

    re_tokens = re.compile(r"""
    \(*\b[^,;#&()]+[.,;)\n]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                       # [^'#abc'] -> ['#']
    """,
                       re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens:
        return []

    return tokens

def term_match(token, list):
    ## Split into individual words
    terms = re.compile(r'[^\s,;\b-]+').findall(token)
    common = set(terms).intersection(set(list))
    return len(common) > 0

def has_ordinal(token):
    match = re.compile(r'[0-9]+[th|st|rd]').findall(token)
    return len(match) > 0

def tokenFeatures(token):
    if token in (u'&', u'#'):
        token_clean = token
    else:
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token,
                             flags=re.UNICODE)

    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {
        'abbrev': token_clean[-1] == u'.',
        'digits': digits(token_clean),
        'word': (token_abbrev
                 if not token_abbrev.isdigit()
                 else False),
        'trailing.zeros': (trailingZeros(token_abbrev)
                           if token_abbrev.isdigit()
                           else False),
        'length': (u'd:' + str(len(token_abbrev))
                   if token_abbrev.isdigit()
                   else u'w:' + str(len(token_abbrev))),
        'endsinpunc': (token[-1]
                       if bool(re.match('.+[^.\w]', token, flags=re.UNICODE))
                       else False),
        'directional': term_match(token_abbrev, DIRECTIONS),
        'street_name': term_match(token_abbrev, STREET_NAMES),
        'locality_name': term_match(token_abbrev, LOCALITY_NAMES),
        'building_name': term_match(token_abbrev, BUILDING_NAMES),
        'landmark_name': term_match(token_abbrev, LANDMARK_NAMES),
        'city_name': term_match(token_abbrev, CITY_NAMES),
        'state_name': term_match(token_abbrev, STATE_NAMES),
        'has_ordinal': has_ordinal(token_abbrev),
        'has.vowels': bool(set(token_abbrev[1:]) & set('aeiou')),
    }

    return features


def tokens2features(address):
    feature_sequence = [tokenFeatures(address[0])]
    previous_features = feature_sequence[-1].copy()

    for token in address[1:]:
        token_features = tokenFeatures(token)
        current_features = token_features.copy()

        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features

        feature_sequence.append(token_features)

        previous_features = current_features

    feature_sequence[0]['address.start'] = True
    feature_sequence[-1]['address.end'] = True

    if len(feature_sequence) > 1:
        feature_sequence[1]['previous']['address.start'] = True
        feature_sequence[-2]['next']['address.end'] = True

    return feature_sequence


def digits(token):
    if token.isdigit():
        return 'all_digits'
    elif set(token) & set(string.digits):
        return 'some_digits'
    else:
        return 'no_digits'


def trailingZeros(token):
    results = re.findall(r'(0+)$', token)
    if results:
        return results[0]
    else:
        return ''


class RepeatedLabelError(probableparsing.RepeatedLabelError):
    REPO_URL = None
    DOCS_URL = None

