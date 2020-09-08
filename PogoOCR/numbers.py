"""This is taken from babel.numbers and modified. The following license applies


Copyright (c) 2013-2019 by the Babel Team, see AUTHORS for more information.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
 3. The name of the author may not be used to endorse or promote
    products derived from this software without specific prior
    written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import decimal
from typing import Dict

from babel.numbers import NumberFormatError


def parse_number(string, locale: Dict[str, str] = dict(group=",", decimal=".")):
    group_symbol = locale.get("group", ",")
    if (
        group_symbol == "\xa0"
        and group_symbol not in string  # if the grouping symbol is U+00A0 NO-BREAK SPACE,
        and " "  # and the string to be parsed does not contain it,
        in string  # but it does contain a space instead,
    ):
        # ... it's reasonable to assume it is taking the place of the grouping symbol.
        string = string.replace(" ", group_symbol)

    try:
        return int(string.replace(group_symbol, ""))
    except ValueError:
        raise NumberFormatError("%r is not a valid number" % string)


def parse_decimal(string, locale: Dict[str, str] = dict(group=",", decimal=".")):
    group_symbol = locale.get("group", ",")
    decimal_symbol = locale.get("decimal", ".")

    if (
        group_symbol == "\xa0"
        and group_symbol not in string  # if the grouping symbol is U+00A0 NO-BREAK SPACE,
        and " "  # and the string to be parsed does not contain it,
        in string  # but it does contain a space instead,
    ):
        # ... it's reasonable to assume it is taking the place of the grouping symbol.
        string = string.replace(" ", group_symbol)

    try:
        parsed = decimal.Decimal(string.replace(group_symbol, "").replace(decimal_symbol, "."))
    except decimal.InvalidOperation:
        raise NumberFormatError("%r is not a valid decimal number" % string)
    return parsed
