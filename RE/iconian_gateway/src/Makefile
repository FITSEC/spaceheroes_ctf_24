server:
	gcc -o server server.c

client:
	tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Virtualize --Functions=win --out=result.c ./client.c && gcc -o client result.c
	rm result.c a.out
