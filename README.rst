LTis diegimas ir klaidų paieška
===============================
1. Aktyvuoti "developer options": https://www.youtube.com/watch?v=3eJXHhploOo
2. Įjungti parinktį "USB debugging", esančią "developer options" skiltyje
3. Parisiųsti ir įsidiegti ``buildozer`` (https://kivy.org/docs/guide/packaging-android.html)
    ``git clone https://github.com/kivy/buildozer.git``
    ``cd buildozer``
    ``sudo python2.7 setup.py install``
4. Įsidiegti ``adb``, nes prijungtas įrenginys gali būti "unauthorized".
    ``sudo apt-get install android-tools-adb android-tools-fastboot``
5. Ir įvykdyti instrukcijas: https://stackoverflow.com/a/25546300/2609806
6. Paleisti ``make deploy``
7. Jeigu programėlė pasileisdama nulūžo, telefono logus galima peržiūrėti įvykdžius
   ``make log`` ir atsidarius ``logcat.txt`` failą, kuris sugeneruojamas
   einamojoje direktorijoje. Ten reikia ieškoti ``Traceback`` žodžio.

Projekto įdėjos
===============
Reklamavimas LaisvėsTV pradžioje.
