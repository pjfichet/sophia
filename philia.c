/*
** Philia:
** Insert refer bibliography references in a file
** using Sophia database.
** Usage:
** philia < file
** Database is actually hardcoded
** Depends on sqlite3.
** Compilation:
** cc -Wall -l sqlite3 -o philia philia.c
**
** $Id$
*/

#include <stdio.h>
#include <string.h>
#include <sqlite3.h>

#define DATABASE "/home/pj/doc/troff/refer/sophia.db"
#define QUERY "SELECT id, bid, A, T, hh, tp FROM alls WHERE id="
#define LQUERY 50


/* printresult:
** print result of the searchsqlite query
** in the refer format.
*/
static int
printresult(void *null, int argc, char **argv, char **col)
{
  /* first "." and last "\n" are printed by readfile */

  printf("@ %s\n", argv[0]); // id
  printf(".[\n");
  //printf("A%sA %s\n", argv[1], argv[2]); // A T
  printf("A%sA %s %s\n", argv[1], argv[2], argv[3]); // bid A T
  printf("%%h %s\n", argv[4]); // hh
  printf("%%p %s\n", argv[5]); //tp
  printf(".]");

  return 0;
}

/* searchsqlite:
** Receive database, id, and line number of text
** where @ macro appears as arguments.
** Query row id in database.
** If result are found, launch printresult,
** else print error message containing line number.
*/
int
searchsqlite(sqlite3 *db, char *id, long line)
{
  char *msg = 0;
  char query[LQUERY] = QUERY; 
  int rc;

  strcat(query, id);

  rc = sqlite3_exec(db, query, printresult, 0, &msg);
  if( rc!=SQLITE_OK ){
    fprintf(stderr, "Line %ld, @ %s: %s\n", line, id, msg);
    sqlite3_free(msg);
    return 1;
  }
  return 0;
}

/* readfile:
** receive database as argument.
** read file and search for macros (\n.)
** If @ macro is found, look its first arg,
** and call searchsqlite with this arg as id,
** the database and the line number as other arguments.
** Else, just print chars to stdout.
*/
int
readfile(sqlite3 *db)
{
  int c;
  int mc = 1;
  char theid[5];
  char *id;
  id=theid;
  long line = 1;
  int rt = 0;

  while( (c=getchar()) != EOF){

    /* look for macros */
    if( c=='\n'){
      mc=1;
      ++line;
    }
    else if( c=='.' && mc==1)
      mc=2;

    /* found philia macro */
    else if( c=='@' && mc==2){
      while( (c=getchar()) == ' ' || c =='\t')
        ;
      if( c == '\n'){
        fprintf(stderr, "Line %ld, @ without id.\n", line);
        ++rt;
      }
      else { 
        id=theid;
        *id++=c;
        /* get first argument */
        while( (c=getchar()) != '\n' && c!=' ' && c!='\t')
          *id++=c;
        *id='\0';
        rt += searchsqlite(db, theid, line);
        /* skip other arguments */
        if( c==' ' || c=='\t')
          while( (c=getchar()) != '\n');
      }
      mc=1;
      ++line;
    }

    /* skip macros */
    else if( mc==2){
      putchar(c);
      while( (c=getchar()) != '\n')
        putchar(c);
      mc=1;
      ++line;
    }

    /* TODO: deal with space and tabs before macros */

    /* default: reset mc */
    else
      mc=0;

    /* print */
    putchar(c);
  } 
  return 0;
}


/*
** main:
** open sqlite database in readonly mode,
** return an error if not possible.
** launch readfile with database as argument.
*/
int
main(void)
{
  sqlite3 *db;
  int rc;
  int rt;
  char *p = NULL;

  /* TODO: read args to get database */

  rc = sqlite3_open_v2(DATABASE, &db, SQLITE_OPEN_READONLY, p);
  if( rc ){
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return 1;
  }

  rt = readfile(db);

  sqlite3_close(db);
  return rt;
}

