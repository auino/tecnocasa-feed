# tecnocasa-feed

This service is intended to be mainly used from Italian persons.
Therefore, this document is written in Italian language.

###Descrizione

Questo programma permette di configurare su un server web in grado di fornire feed in formato [RSS](https://it.wikipedia.org/wiki/RSS) dei risultati ottenuti dal sito di [Tecnocasa](http://tecnocasa.it), per specifiche ricerche personalizzabili.
Siccome il sito ufficiale di Tecnocasa non fornisce (ad oggi, al meglio della conoscenza del sito da parte dello sviluppatore) un servizio di [API](https://it.wikipedia.org/wiki/Application_programming_interface) o [feed](https://it.wikipedia.org/wiki/Feed) RSS (cosa che ad esempio [Immobiliare.it](http://immobiliare.it) offre), questo programma permette di sopperire a questa mancanza, ponendosi tra il sito ufficiale di Tecnocasa e un comune [feed reader](https://it.wikipedia.org/wiki/Aggregatore).

Per chi non conoscesse Tecnocasa, si tratta di una agenzia immobiliare largamente diffusa sul territorio italiano.
Maggiori informazioni sono disponibili sul sito ufficiale [www.tecnocasa.it](http://www.tecnocasa.it).

Occorre sottolineare che lo sviluppatore non è in alcun modo affiliato a Tecnocasa.

####Dettagli tecnici

Il programma fa uso di tecniche di [parsing](https://it.wikipedia.org/wiki/Parsing) (attraverso la libreria [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)) per analizzare il contenuto (sotto forma di [DOM](https://it.wikipedia.org/wiki/Document_Object_Model)) del sito mobile di Tecnocasa](http://m.tecnocasa.it).
Siccome l'approccio seguito si basa su una analisi sintattica, il sistema non è da ritenersi affidabile nel caso di modifiche alla struttura delle pagine analizzate.

###Setup del server

Da notare che, sebbene il programma sia da intendersi principalmente per un pubblico italiano, il codice ed i commenti in esso presenti sono scritti in lingua inglese.

####Prerequisiti

Il programma è scritto in Python ed utilizza le seguenti librerie:
 * `web.py`
 * `requests`
 * `BeautifulSoap`
 * `datetime`

TODO

####Configurazione

TODO

####Esecuzione

E' possibile avviare il server web attraverso il seguente comando:

```
python tecnocasa.py
```

Il server resterà in questo caso in ascolto sulla porta `8080`, la porta di default.

Se si desidera adottare un'altra porta (ad esempio, la porta `1234`), è possibile avviare il server attraverso il seguente comando:

```
python tecnocasa.py 1234
```

####Pagina principale

Il server web fornisce una pagina principale (generalmente nota come `index`), visitabile al seguente indirizzo:

```
http://ip_server:8080/
```

dove si assume che il server sia in ascolto sulla porta di default `8080`, e dove `ip_server` identifica l'indirizzo del server.

Questa pagina reindirizza l'utente alla [pagina principale del progetto](https://github.com/auino/tecnocasa-feed) su GitHub.

####Formato del feed

TODO

###Esempio di utilizzo

TODO

###Contatti

Puoi trovarmi su Twitter come [@auino](https://twitter.com/auino).
