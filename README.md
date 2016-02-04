[Versione parzialmente incompleta]

# tecnocasa-feed

This service is intended to be mainly used from Italian persons.
This document is therefore written in Italian language.
Nevertheless, code and included comments are in English language.

###Descrizione

Questo programma permette di configurare su un server web in grado di fornire feed in formato [RSS](https://it.wikipedia.org/wiki/RSS) dei risultati ottenuti dal sito di [Tecnocasa](http://tecnocasa.it), per specifiche ricerche personalizzabili.
Siccome il sito ufficiale di Tecnocasa non fornisce (ad oggi, al meglio della conoscenza del sito da parte dello sviluppatore) un servizio di [API](https://it.wikipedia.org/wiki/Application_programming_interface) o [feed](https://it.wikipedia.org/wiki/Feed) RSS (cosa che ad esempio [Immobiliare.it](http://immobiliare.it) offre), questo programma permette di sopperire a questa mancanza, ponendosi tra il sito ufficiale di Tecnocasa e un comune [feed reader](https://it.wikipedia.org/wiki/Aggregatore).

Per chi non conoscesse Tecnocasa, si tratta di una agenzia immobiliare largamente diffusa sul territorio italiano.
Maggiori informazioni sono disponibili sul sito ufficiale [www.tecnocasa.it](http://www.tecnocasa.it).

Occorre sottolineare che lo sviluppatore non è in alcun modo affiliato a Tecnocasa.

####Approccio seguito

Il programma fa uso di tecniche di [parsing](https://it.wikipedia.org/wiki/Parsing) (attraverso la libreria [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)) per analizzare il contenuto (sotto forma di [DOM](https://it.wikipedia.org/wiki/Document_Object_Model)) del [sito mobile di Tecnocasa](http://m.tecnocasa.it).
Pertanto, siccome l'approccio seguito si basa su una analisi sintattica, il sistema non è da ritenersi affidabile nel caso di modifiche alla struttura delle pagine analizzate.

Il parsing è effettuato a run-time, dunque le informazioni vengono recuperate al momento della richiesta dell'utente.
Sebbene una soluzione di questo tipo porti a tempi di risposta più elevati, essa è in grado di fornire sempre una versione aggiornata dei risultati e non richiede l'adozione di tecniche di caching.

###Setup del server

Da notare che, sebbene il programma sia da intendersi principalmente per un pubblico italiano, il codice ed i commenti in esso presenti sono scritti in lingua inglese.

####Download

Per installare il software eseguire il seguente comando da terminale:

```sh
git clone https://github.com/auino/tecnocasa-feed.git
```

Una directory di nome `tecnocasa-feed` verrà creata.

A questo punto è possibile accedere alla directory creata con il seguente comando:

```sh
cd tecnocasa-feed
```

####Prerequisiti

Il programma è scritto in Python ed utilizza le seguenti librerie:
 * [web.py](http://webpy.org) to host the web service
 * [requests](http://docs.python-requests.org/en/master/) to communicate with Tecnocasa servers
 * [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to parse HTML contents

Per installare le librerie necessarie, eseguire il seguente comando da terminale:

```sh
sudo pip install -r requirements.txt
```

####Configurazione

TODO

####Esecuzione

E' possibile avviare il server web attraverso il seguente comando:

```sh
python tecnocasa.py
```

Il server resterà in questo caso in ascolto sulla porta `8080`, la porta di default.

Se si desidera adottare un'altra porta (ad esempio, la porta `1234`), è possibile avviare il server attraverso il seguente comando:

```sh
python tecnocasa.py 1234
```

####Pagina principale

Il server web fornisce una pagina principale (generalmente nota come `index`), visitabile al seguente indirizzo:

```php
http://$ip_server:8080/
```

dove si assume che il server sia in ascolto sulla porta di default `8080`, e dove `$ip_server` identifica l'indirizzo del server.

Questa pagina reindirizza l'utente alla [pagina principale del progetto](https://github.com/auino/tecnocasa-feed) su GitHub.

####Pagina del feed

Il server web permette di recuperare un feed RSS personalizzato, visitabile al seguente indirizzo:

```
http://$ip_server:8080/feed/?lat=$lat&lon=$lon&radius=$radius&price=$price&size=$size&description=$description
```

dove si assume che il server sia in ascolto sulla porta di default `8080`, e dove `$ip_server` identifica l'indirizzo del server.

La pagina richiede pertanto il passaggio in input delle seguenti informazioni (tutti i parametri sono obbligatori):
 * le coordinate di un punto di riferimento su mappa, sotto forma di latitudine (parametro `$lat`) e longitudine (parametro `$lon`)
 * il raggio considerato per la ricerca di offerte (parametro `$radius`), in chilometri
 * il prezzo massimo da considerare (parametro `$price`), senza punti o virgole
 * la dimensione minima in metri quadri (parametro `$size`)
 * la descrizione della query (parametro `$description`), utilizzata all'interno del titolo del feed

Per quanto riguarda il recupero dei parametri relativi alle coordinate, questi possono essere identificati in vari modi:
 1. Attraverso l'utilizzo di siti appositi come [getlatlon.yohman.com](http://getlatlon.yohman.com)
 2. Direttamente dal [sito mobile di Tecnocasa](http://m.tecnocasa.it), effettuando una ricerca ed analizzando i parametri passati nell'indirizzo

Il formato di output del feed è fornito da [templates/feed.html](https://github.com/auino/tecnocasa-feed/blob/master/templates/feed.html).

###Esempio di utilizzo

Assumendo che si voglia fare una ricerca (denominata `RomaCentro`) in un raggio di `5` chilometri dal centro di Roma (associato a latitudine `41.91022566604198` e longitudine `12.535997900000098`), per immobili di almeno `60` metri quadri e di valore non superiore a `250000` €, il corretto indirizzo del feed sarebbe il seguente:

```
http://$ip_server:8080/feed/?lat=41.91022566604198&lon=12.535997900000098&radius=5&price=250000&size=60&description=RomaCentro
```

dove si assume che il server sia in ascolto sulla porta di default `8080`, e dove `$ip_server` identifica l'indirizzo del server.

Questo indirizzo può essere fornito in input ad un aggregatore di feed RSS, come ad esempio [Reeder](http://reederapp.com) o [Feedly](http://feedly.com).

###Contatti

Sono disponibile su Twitter come [@auino](https://twitter.com/auino).
