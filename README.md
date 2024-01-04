# TKOM 23Z

Karol Kasperek

Język programowania: Python

Temat: 
Język z typem walutowym

Opiekun projektu: dr inż. Piotr Gawkowski

## Uruchomienie projektu

Aby prawidłowo uruchomić projekt należy wpisać w terminal komende: python3.11 src/main.py {ścieżka do pliku} znajdując sie w głównym folderze projektu.

## Założenia podstawowe
- dynamicznie typowany
- słabo typowany
- zmienne są mutowalne
- tworzenie zmiennych oraz przypisanie do nich wartości znakiem '='
- brak składniowego rozdzielenia deklaracji zmiennej oraz przypisania wartości
- podstawowe typy liczbowe (int, float), operacje matematyczne zachowujące kolejność działań i nawiasowanie
- podstawowy typ znakowy (string), konkatenacja dwóch łańcuchów znakowych
- komentarz w linijce oznaczony znakiem `#` (rozpoczęcie w dowolnym miejscu, koniec wraz z końcem linii)
- definiowanie własnych funkcji (wartość do funkcji przekazywana przez referencje)
- bloki kodu ograniczone przez nawias klamrowy
- wyrażenia oraz instrukcje zakończone średnikiem
- podstawowe typy danych: int, float, bool, string
- dodatkowy typ danych: typ walutowy, zawierający atrybut currency_type, odwołanie po kropce podane w przykładach kodu, brak mutowalności
- funkcja może wywoływać siebie samą (rekursja)
- plik z kodem źródłowym zawierają pojedyńczy punkt wejścia 'main()'
- można odwoływać się do funkcji zdefiniowanych przed i po bloku
- obsługiwanie jedynie definicji funkcji znajdujących się w pliku
- intrukcja warunkowa 'if' z 'else'
- instrukcja pętli 'while'
- instrukcje sterujące return, break, continue
- możliwość wypisywania danych na standardowe wyjście - funkcja 'print()'
- wczytywanie danych od użytkownika za pomocą funkcji 'input()'
- obsługa błędów
- obsługa operatorów arytmetycznych +,-,*,/,^
- obsługa operatorów porównujących <,>,<=,>=,==,!=
- obsługa operatorów logicznych ||, &&, !
- operator przewalutowania ->, priorytet na poziomie priorytetu operatora potęgowania
- pobieranie aktualnych kursów walutowych ze strony i tworzenie macierzy pomiędzy nimi (macierz będzie zawierać informacje o kursie przewalutowania pomiędzy konkretnymi walutami)


## Założenia niefunkcjonalne

- leniwa tokenizacja - umożliwi to przetwarzanie dużych plików
- projekt zaimplementowany w języku python
- podział na 3 moduły - lekser, parser oraz interpreter
- operatory - realizacja priorytetów operatorów zgodna z dokumentacją języka C++ - https://en.cppreference.com/w/cpp/language/operator_precedence
- stworzenie oddzielnego modułu zarządzającego błędami
- kursy walut powinny być aktualizowane minimum raz dziennie
- obsługa wielu walut


## Podstawowe instrukcje języka

### Instrukcja warunkowa

Obsługiwanie podstawowe instrukcji warunkowej:

```
if(5 > 4){
    print(6);    
}
```

### Pętla

Obsługa podstawowej pętli (while): 

```
while(5 > 4){
    print(6);
}
```
## Założenia dodatkowe

Mój język ma na celu udostępnienie dodatkowych opcji odnośnie wykonywania operacji na międzynarodowych systemach walutowych. W moim języku zostaną zaimplementowane dodatkowe zmienne, które będą umożliwiały zapisywanie wartości w innych walutach. Przykładowy kod zostanie podany niżej. Dane o kursach walutowych będą pobierane ze strony internetowej oraz będzie tworzona macierz zależności tych kursów pomiędzy sobą. Będzie to uproszczało operacje, ponieważ będzie można odwoływać się do poszczególnych pól, zamiast wykonywać operacje przewalutowania. Interpreter będzie przetrzymywał typ walutowy w postaci ENUM.

## Zakres zmiennych

Deklaracja zmiennych może odbywać się w dowolnym funckji w programie. Jednak wraz z opuszczeniem danego bloku kodu, wszystkie zmienne stworzone w nim zostaną utracone i ich nazwy zostaną zwolnione w pozostałej części kodu.

## Gramatyka

- program                   = {function_definition};
- function_definition     	= id, "(", [parameter_list], ")", block;
- id                        = letter, {letter | digit | "_"};
- argument_list				= expression, {",", expression};
- parameter_list			= id, {",", id};
- block                     = "{", {statement}, "}"
- statement                 = variable_access | if_statement | while_statement | assignment, ";" | break, ";" | continue, ";" | return_statement; 
- variable_access 			= function_call, ".", function_call;
- assignment               	= id, "=", expression;
- function_call             = id, ["(", [argument_list], ")"];
- if_statement              = "if", "(", expression, ")", block, ["else", block];
- while_statement           = "while", "(", expression, ")", block;
- return_statement          = "return", [expression];
- expression				= or_term , ["||", or_term];
- or_term					= and_term, ["&&", and_term];
- and_term					= ["!"], comparison;
- comparison				= additive_expression, [("==" | "!=" | ">=" | "<=" | "<" | ">"), additive_expression];
- additive_expression       = multiplicative_expression, {"+" | "-"}, multiplicative_expression;
- multiplicative_expression	= factor, {"*" | "/"}, factor;
- factor					= exponent_factor, {("^" | "->"), exponent_factor};
- exponent_factor			= [-], numeric_term;
- numeric_term				= constant | "(", expression, ")" | variable_access;
- constant 					= num_const | bool_const | string_const | currency_const;
- currency_const			= num_const , currency_id;
- num_const					= non_zero_digit, {digit}, [".", {digit}];
- bool_const				= "true" | "false";
- string_const				= '"', {char}, '"';
- currency_id				= {char}; 									# będzie znajdował się w ścisłym zakresie nazw zapisanych w konfiguracji
- char						= {not_zero_digit | not_digit | zero_digit};
- zero_digit				= "0";
- not_zero_digit			= "1" | "2" | "3" | ...;
- not_digit					= "A" | "B" | ... | "z" | "$" | "@" | ...;




## Przykładowy kod

### Przypisanie wartości do zmiennej
```
main()
{
	var_int = 5;
	var_bool = true;
	var_float = 5.5;
	var_string = 'string';
}
```
### Wypisywanie wartości 
```
main()
{
	print(var_int); # 5
	print(var_bool); # true
	print(var_float); # 5.5
	print(var_string); # string
}
```

### Konkatenacja łańcuchów znaków
```
main()
{
	str = 'poczatek';
	str2 = 'koniec';
	str3 = str + str2;
	print(str3); # poczatekkoniec
	print(str + str2); # poczatekkoniec
}
```

### Komentarz kodu

```
main()
{
	x = 5; # tutaj jest komentarz
}
```

### Dostępność zmiennych

```
mian()
{
	cost = 21;
	tax = cost * 0.1;
	totalCost = tax + cost;
	if(totalCost > 20)
	{
		diff = totalCost - 20;
		print(diff); # 3.1
	}
	print(diff); # zmienna już nie istnieje
}
```
### Definiowanie własnej funkcji ze zwracaniem wartości oraz wywołanie

```
func(x)
{
	return x * x;
}

main()
{
	y = 5;
	result = func(y);
	print(result); # 25
}

```
### Rekursja

```
func(x)
{
	if(x > 5){
		func(x - 1);
	}
	return 10;
}

main()
{
	func(8); # 10
	a = 5;
	func(a);
}
```

### Przekazywanie przez referencje
```
func(x)
{
	x = x + 5;
}

main()
{
	y = 4;
	func(y); # y = 9;
	z = y * 4; # z = 36;
}
```
### Kolejność wykonywania działań
```
main()
{
	x = (2 * 2) + 2 / 2; # x == 5
	y = 5 * 5 / 5 + 5 * (2 + 1); # y == 20
	z = (8 + 8) / (4 + 4); # z == 2
}
```
### Stworzenie typu walutowego
```
main()
{
	a = 20.20 EUR;
	b = 40 USD;
}
```
### Operacje na zmiennych walutowych
```
main()
{
	a = 20.20 EUR;
	b = 40 USD;
	a = a * 0.5; # 10.10 EUR
	b = b + 20 USD; # 60 USD
	c = a + b; # w takim przypadku dodawanie sprowadzi walutę do typu waluty pierwszej zmiennej
	x = b + 20 EUR; # tak samo jak powyżej, zostanie zamieniona na typ waluty b
	d = 200 PLN;
	d = d -> USD; # zmienna D zostanie w takim wypadku przewalutowana i zamieniona na USD
	e = a -> d.currency_type; # wartośc ze zmiennej a zostanie przewalutowana na typ waluty ze zmiennej d i zapisana w zmiennej e
	f = 20 PLN;
}
	
```

### Escaping stałych znakowych
```
main()
{
	print("Przykładowy tekst\""); # Przykładowy tekst"
}
```
### Przykładowy wygląd programu
```
main()
{
	x = 5;
	y = 'abc';
	yy = 'xyz';
	z = 5.5;

	b = y + yy;
	c = 'abcxyz';
	if(b == c)
	{
		print(x);
	}
	else
	{
		while(x > 2)
		{
			print(x);
			x = x - 1;
		}
	}
    
    return 0;
}
```

## Przykładowe fragmenty błędnego kodu

### Błąd porównania
```
main()
{
	x = 5;
	y = 'ABC';
	if(x > y)
	{
		print(1);
	}
}
```

### Błąd przypisania zmiennej
```
main()
{
	x = '5;
	print(x);
}
```

## Obsługa błędów

W przypadku napotkania błędu podczas pracy lexera/parsera/interpretera, error manager agreguje i dzieli błędy na krytyczne i niekrytyczne. Error manager będzie przekazywany do modułów w konstruktorze. Error manager w momencie napotkania błędu krytycznego podniesie wyjątek, który będzie obsłużony na zewnątrz, natomiast gdy błąd jest niekrytyczny, użytkownik otrzyma informację o jego wystąpieniu, jednak program może dalej wykonywać się poprawnie.

### Lekser:
#### Niekrytyczne
- Overflow 			- przekroczenie zakresu liczbowego (Overflow in line {10}, column {20})
- UnknownToken 		- token jest nierozpoznany (Unknown token {name} in line {10}, column {20})
- StringTooLong 	- ciąg znaków jest za długi (String too long in line {10}, column {20})
- InfiniteString 	- brak kończącego cudzysłowia dla typu string (String without end startin in line {10}, column {20})


### Parser
#### Krytyczne
- UnexpectedToken 	- tokeny w niepoprawnej kolejności względem przyjętej gramatyki (Unexpected Token {string} in line {10}, column{20})
- DuplicateDefinition - ponowna definicja funkcji o tej samej nazwie (Duplicate function {name} in line {10}, column {20})
- ExpectingIdentifier - oczekiwano identyfikatora, a otrzymano inny symbol (Expecting identifier in line {10}, columnt {20})
- ExpectingExpression - oczekiwano wyrażenia, a otrzymano inny symbol (Expecting expression in line {10}, columnt {20})
#### Niekrytyczne
- MissingSemicolon - brak średnika {Missing semi-colon in line {10}, column {20}}

### Interpreter
#### Krytyczne
- DivisionByZero - dzielenie przez zero (Division by zero try in line {10}, column {20})
- UndefinedVariable - użyto zmiennej, która nie została jeszcze zadeklarowana (No variable {name} in scope or not defined in line {10}, columnt {20})
- WrongTypeForOperation - operacja na obiekcie innego niż typu numerycznego lub logiczny (Operation between types {string} and {int} is not allowed in line {10}, column {20})
- NotExactArguments - liczba argumentowych w funckji jest niepoprawna (Not exact number of arguments in line {10}, column {20})
- FunctionNotFound - funkcja o takiej nazwie nie istnieje (Function not found {name} in line {10}, columnt {20})
- NoMainFunction - brak funckcji wejścia (File doesn't have main function)


## Struktura projektu
- Lekser - przetwarzanie tekstu na tokeny
- Parser - budowanie struktury obiektów z tokenów otrzymanych od leksera
- Interpreter - wykonywanie kodu, dołącznie zewnętrznych typów
- Testy - przy użyciu pytest
- Error Manager - obsługa błędów w kodzie

Interface pomiędzy lekserem, a parserem będzie wyglądał w następujący sposób. Główny plik stworzy konieczne obiekty (lexer, parser itp.), a następnie wywoła metodę parse(), która spowoduje przechodzenie przez plik tekstowy otrzymany do interpretacji i przetworzy na bieżąco otrzymane tokeny w drzewo AST. Gdy praca z aktualnym tokenem zakończy się, wykonana zostanie metoda next() w lekserze. Dzięki temu uzyskamy leniwą tokenizację. Każdy z modułów może również zgłosić błąd, przy użyciu obiektu ErrorManagera. Został zaimplementowany również oddzielny moduł, którego zadaniem jest wykonywanie obliczeń podanych przez interpreter w czasie przetwarzania pliku wejściowego. Obsługuje on operacje dla wszystkich typó zmiennych (waluta, int, string, bool).


## Testowanie
Do testów jednostkowych użyje biblioteki pytest.
Projekt zamierzam testować zgodnie z popularną konwencją: 
- Testy jednostkowe - do poszczególnych funkcji
- Testy integracyjne - sprawdzające połączenia między elementami
- Testy akceptacyjne - działanie końcowego programu, będę one rozszerzeniem kodu zawartego w dokumentacji wstępnej, mają one na celu sprawdzenie wszystkich podstawowych założeń języka takich jak: 
- - tworzenie zmiennych
- - instrukcja warunkowa i pętla
- - operatory arytmetyczne
- - rekursja
- - kolejność wykonywania działań
- - zamiana walut oraz działania na nich
- - konkatenacja stringów
- - przekazywanie zmiennych przez referencje
Do testów akceptacyjnych użyję również fragmentów kodu zawartych w dokumentacji. Podczas testowanie zostanie on jednak rozszerzony.