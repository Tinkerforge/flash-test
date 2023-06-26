# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_base.py: Base for Bricklets

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import os
import socket
import traceback
from datetime import datetime
import psycopg2 # pip install psycopg2
from tzlocal import get_localzone
from PyQt5 import QtWidgets

HOST = '192.168.178.12'
DBNAME = 'foobar'
USER = 'postgres'

def insert_report(parent, postgres_password, sku, uid, firmware_version, hardware_version):
    created_on = datetime.now(tz=get_localzone()).isoformat()
    hostname = socket.gethostname()

    sql = """INSERT INTO flash_test_reports(created_on, hostname, username, sku, uid, firmware_version, hardware_version)
             VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    conn = None

    try:
        conn = psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=postgres_password)
        cur = conn.cursor()
        cur.execute(sql, (created_on, hostname, '', sku, uid, firmware_version, hardware_version))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        QtWidgets.QMessageBox.critical(parent, 'Datenbankproblem', 'Konnte Report nicht eintragen:\n\n' + traceback.format_exc())
    finally:
        if conn != None:
            conn.close()

def main():
    from tinkerforge.device_display_names import get_device_display_name

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'postgres_password.txt'), 'rb') as f:
        postgres_password = f.read().decode('utf-8').split('\n')[0].strip()

    try:
        conn = psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=postgres_password)
        cur = conn.cursor()
        cur.execute('SELECT * FROM flash_test_reports;')

        rows = list(cur.fetchall())

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        QtWidgets.QMessageBox.critical(parent, 'Datenbankproblem', 'Konnte Report nicht eintragen:\n\n' + traceback.format_exc())
    finally:
        if conn != None:
            conn.close()

    by_date = {}

    for row in rows:
        row = list(row)
        row[0] = row[0].astimezone(get_localzone())

        by_date.setdefault(row[0].date(), []).append(tuple(row))

    for date, rows in by_date.items():
        print()
        print(date, len(rows))

        for row in rows:
            created_on, hostname, username, sku, uid, firmware_version, hardware_version = row
            print(f'  {created_on.isoformat()}   {hostname}   {username if len(username) > 0 else "?"}   {get_device_display_name(int(sku))}   {uid}   {firmware_version}   {hardware_version if len(hardware_version) > 0 else "?"}')

if __name__ == '__main__':
    main()
