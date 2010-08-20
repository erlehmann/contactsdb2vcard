#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pysqlite2 import dbapi2 as sqlite
import vobject

connection = sqlite.connect('contacts.db')
cursor = connection.cursor()

STATEMENT = 'SELECT _id, name FROM people'
people = cursor.execute(STATEMENT).fetchall()

for person in people:
    if person[1] != None:
        id = person[0]

        name = person[1]
        family = name.split()[-1]
        given = name.split()[0]

        vcard = vobject.vCard()
        vcard.add('fn').value = name

        if family != given:
            vcard.add('n').value = vobject.vcard.Name(family=family, given=given)
        else:
            vcard.add('n').value = vobject.vcard.Name(family='', given=given)

        STATEMENT = 'SELECT person, number FROM phones WHERE person = ' + str(id)
        phones = cursor.execute(STATEMENT).fetchall()

        for phone in phones:
            number = phone[1]
            number = number.replace(' ','') # normalize numbers
            number = number.replace('+','00') # global numbers, android import error when + is used

            vcard.add('tel').value = 'tel:' + number

        STATEMENT = 'SELECT kind, data FROM contact_methods WHERE person = ' + str(id)
        contact_methods = cursor.execute(STATEMENT).fetchall()

        for contact_method in contact_methods:
            kind = contact_method[0]
            data = contact_method[1]

            if kind == 1:
                vcard.add('email').value = data
            if kind == 2:
                data.encode('ascii', 'replace')
                data = data.replace(',','')
                data = data.replace('\n',' ')
                vcard.add('adr').value = vobject.vcard.Address(street=data, city='', region='', code='', country='', box='', extended='')
            if kind == 3:
                vcard.add('impp').value = 'xmpp:' + data

        print vcard.serialize()
        #vcard.prettyPrint()

