/*
** Quote: version temporaire de sophia.c
*/

#include <stdio.h>
#include <stdlib.h>

/*
** Build array of datas from command line
** Get command from command line
** Fetch sqlite database
** Output the text

int
main(int argc, char **argv)		/* process command-line arguments */
{
	while (argc > 1 && argv[1][0] == '-') {
		switch(argv[1][1]) {
		case 'e':
			break;
		case 's':
			break;
		case 'i':
			break;
		case 'l': 
			s = argv[1]+2;
			nmlen = atoi(s);
			while (*s)
				if (*s++ == ',')
					break;
			break;
		case 'k':
			keywant = (argv[1][2] ? argv[1][2] : 'L');
			break;
		case 'n':
			break;
		case 'p':
			argc--; 
			argv++;
			break;
		case 'a':
			authrev = atoi(argv[1]+2);
			break;
		case 'b':
			bare = (argv[1][2] == '1') ? 1 : 2;
			break;
		case 'c':
			smallcaps = argv[1]+2;
			break;
		case 'd':
			newsmallcaps = argv[1]+2;
			break;
		case 'f':
			refnum = atoi(argv[1]+2) - 1;
			break;
		case 'B':
			if (argv[1][2])
			break;
		case 'S':
			break;
		case 'P':
			break;
		}
		argc--; 
		argv++;
	}

}

