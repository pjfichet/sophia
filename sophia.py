#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
module sophia
manage a database of texts

import sophia_class
so=sophia_class.sophia(database)
	# default database is sophia.db
so.insert(dict)
	# return a list containing one dict of datas inserted
so.edit(dict)
	# dict must contain "id:value"
	# return a list containing one dict of datas as they are after edition
so.search(dict)
	# return a list of dicts
so.print(dict)
	# return a list of dict of the content of the whole table
	# or return a list of dict of the selected row

dict has the form {key:value}

One of the keys may define the table:
{ table:books } or { table:texts }
But usually, sophia will deduce it from the keys.

In table books, keys are:
{ id: auto increment id,
A:author, B:book, C:city, D:date, E:editor, G:ISBN/ISSN,
H:publication, I:issuer, J:journal, K:keyword, M:collection
N:journal number, O:other, P:pages of book
Q:author if author is not a person, R:report number
S:serie title, T:title, U:co-author, V:volume
w:electronic access type, x:url, y:update, z:last access } 

In table texts, keys are:
{ id:auto increment id, bid:id of book,
ts:title of this text, tg:some tags to easily search,
th:chapter heading of this text, tp:page of this text,
tt:the text }

Some fields are used by refer, but not by sophia:
F:number of reference, L:label, X: annotation,
o:first occurence of citation in isobib

"""


# depends on: python, sqlite3
import os.path
import sqlite3


# optionnaly depends on psyco
try:
	import psyco
	psyco.full()
except ImportError:
	pass

class TableError(Exception):
	"""	Exception concerning table:
		No table with the column x
		Cannot insert in table alls
		Cannot modify table alls
		You must specify an id to edit
	"""

	def __init__(self, text):
		self.text = text

	def __str__(self):
		return self.text


class sophia:
	""" Simple interface to deal with a database of texts.
		User can use functions: insert(), edit(), search(), print()
		But should'nt use: sqlite(), deftable(), create(), makedict()
	"""

	def __init__(self, db="sophia.db"):
		""" init variables """

		if db != "sophia.db":
			self.db = db
		else:
			if not os.path.exists(db):
				try:
					self.db = os.environ["SOPHIA_DB"]
				except KeyError:
					self.db = "sophia.db"
			else:
				self.db = db

		self.tables = {}
		self.tables["texts"] = ("id", "hid", "ts", "tg", "tp", "tt")
		self.tables["heads"] = ("id", "bid", "hh", "hp")
		self.tables["books"] = ("id", "A", "A2", "A3", "B", "C", "D", "E",
		"E2", "E3", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
		"Q", "R", "S", "T", "U", "V", "w", "x", "y", "z")
		# alls is texts + books with only one id, so remove first item of books
		self.tables["alls"] = self.tables["texts"] + self.tables["heads"][1:] \
		+ self.tables["books"][1:]

		if not os.path.exists(self.db):
			self.create()


	def sqlite(self, query, values=None):
		"""Shortcut to execute sqlite query"""
		con = sqlite3.connect(self.db)
		cur=con.cursor()
		# use the following to get a case sensitive database:
		#cur.execute("PRAGMA case_sensitive_like = 1;")
		#con.commit()
		if values == None:
			cur.execute(query)
		else:
			cur.execute(query, values)
		self.lastid=cur.lastrowid
		self.result = cur.fetchall()
		con.commit()
		con.close()


	def create(self):
		"""Create database"""
		view = "CREATE VIEW alls AS SELECT\n texts.id, "
		for table in ("texts", "heads", "books"):
			query = "CREATE TABLE " + table
			query = query + "\n (id INTEGER PRIMARY KEY, "
			# id is yet defined in query, so remove it with [1:]
			for column in self.tables[table][1:]:
				if column == "hid" or column == "bid" or column == "hp" :
					coltype = " INTEGER, "
				else:
					coltype = " TEXT, "
				query = query + column + coltype
				view = view + table + "." + column + ", "
			query = query[:-2] + ");"
			self.sqlite(query)
		view = view[:-2] + """
FROM texts, heads, books
WHERE texts.hid = heads.id AND heads.bid = books.id
ORDER BY A, E, T, texts.id;"""
		self.sqlite(view)

		print ("Database", self.db, "created.")


	def deftable(self, indict):
		"""Define table using indict"""
		self.table=""
		# table might be defined in indict:
		try:
			self.table = indict["table"]
			del indict["table"]
		except KeyError:
			pass
		# always verify that fields are valids:
		for key in indict:
			if key != "id":
				if self.table != "alls" and self.table != "books" \
				and self.table != "heads" and key in self.tables["texts"] :
					self.table = "texts"
				elif self.table != "alls" and self.table != "texts" \
				and self.table != "heads" and key in self.tables["books"] :
					self.table = "books"
				elif self.table != "alls" and self.table != "texts" \
				and self.table != "books" and key in self.tables["heads"] :
					self.table = "heads"
				elif key in self.tables["alls"]:
					self.table = "alls"
				else:
					raise TableError("No table with the column", key)
		if self.table == "":
				self.table = "alls"

		
	def makedict(self):
		"""Make a list of dict to easyly print results"""
		outlist=[]
		for row in self.result:
			outdict= {}
			outdict["table"] = self.table
			i = 0
			for key in self.tables[self.table]:
				if row[i] != None:
					outdict[key] = row[i]
				i = i + 1
			outlist.append(outdict)
		return outlist


	def insert(self, indict):
		"""Insert into table"""
		self.deftable(indict)
		if self.table == "alls":
			raise TableError("Cannot insert in table alls")
		query = "INSERT INTO " + self.table + " (" 
		query_val = ""
		values = []
		for key in indict:
			query = query + key + ", "
			query_val = query_val + "?,"
			values.append(indict[key])
		query = query[:-2] + ") VALUES (" + query_val[:-1] + ");"
		self.sqlite(query, values)

		#indict['id'] = self.lastid
		#print(indict)
		return self.print({'table':self.table, 'id':self.lastid})

	def edit(self, indict):
		"""Update table"""
		self.deftable(indict)
		if self.table == "alls":
			raise TableError("Cannot modify table alls")
		try:
			id = indict["id"]
			del indict["id"]
		except KeyError:
			raise TableError("You must specify an id to edit")
		values = []
		query = "UPDATE " + self.table + " SET "
		for key in indict:
			query = query + key + "=?, "
			values.append(indict[key])
		query = query[:-2] + " WHERE id=?;"
		values.append(id)
		self.sqlite(query, values)
		return self.print({'table':self.table, 'id':id})

	def search(self, indict):
		"""Search for text"""
		self.deftable(indict)
		#query = "SELECT id, "
		query = "SELECT "
		for column in self.tables[self.table]:
			query = query + column + ", "
		query = query[:-2] + " FROM " + self.table + " where "
		values = []
		for key in indict:
			query = query + key + " like ? AND "
			values.append("%" + indict[key] + "%")
		query = query[:-4] + ";"	

		self.sqlite(query, values)
		return self.makedict()

	def head(self, indict):
		"""Search head id from bookid and page"""
		query = "SELECT * FROM heads WHERE bid = ? AND hp <= ? ORDER BY hp;"
		self.sqlite(query, (indict["bid"], indict["p"]))
		self.table='heads'
		self.result=(self.result[-1],) # last
		return self.makedict()

	def print(self, indict):
		"""Print content of row or whole table"""
		self.deftable(indict)
		try:
			# if an id is defined, print row
			query = "SELECT * FROM " + self.table + " WHERE id = ?"
			self.sqlite(query, (str(indict["id"]),))
		except KeyError:
			# else, print all table
			query = "SELECT * FROM " + self.table
			self.sqlite(query)
		return self.makedict()



def main(db):
	sophia(db)

if __name__ == '__main__':
	status = main()
	sys.exit(status)
