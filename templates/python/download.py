{% load my_tags %}################################################################@@#
# {{ problem.title }} {% if problem.description %}
#
# {{ problem.description|markdown2py|safe }}{% endif %}
################################################################@@#

{% for part in parts %}
################################################################@{{ part.id|stringformat:'06d'}}#
# {{ forloop.counter }}) {{ part.description|markdown2py|safe }}
################################################################{{ part.id|stringformat:'06d'}}@#
{% with solutions|get:part.id as solution %}{% if solution %}{{ solution|safe }}{% endif %}{% endwith %}

{% endfor %}








































































































#####################################################################@@#
# Kode pod to črto nikakor ne spreminjajte.
########################################################################

"TA VRSTICA JE PRAVILNA."
"ČE VAM PYTHON SPOROČI, DA JE V NJEJ NAPAKA, SE MOTI."
"NAPAKA JE NAJVERJETNEJE V ZADNJI VRSTICI VAŠE KODE."
"ČE JE NE NAJDETE, VPRAŠAJTE ASISTENTA."



























































{% include 'python/check.py' %}

def _check():
    with open(os.path.abspath(sys.argv[0])) as f:
        source = f.read()

    Check.initialize([
        {
            'part': int(match.group(1)),
            'solution': match.group(2).strip()
        } for match in re.compile(
            r'#{50,}@(\d+)#' # beginning of header
            r'.*?'            # header
            r'#{50,}\1@#'    # end of header
            r'(.*?)'          # solution
            r'(?=#{50,}@)',   # beginning of next part
            flags=re.DOTALL|re.MULTILINE
        ).finditer(source)
    ])

    {{ problem.preamble|indent:"    "|safe }}
    {% for part in parts %}
    if Check.part():
        {{ part.validation|indent:"        "|safe }}
    {% endfor %}

    Check.summarize()
    {% if authenticated %}
    print('Shranjujem rešitve...')
    post = urlencode({
        'data': '{{ data|safe }}',
        'signature': '{{ signature }}',
        'attempts': Check.dump(),
        'source': source,
    }).encode()
    try:
        r = urlopen('http://{{ request.META.HTTP_HOST }}{% url upload %}', post)
        print(r.read().decode())
    except HTTPError:
        print('Pri shranjevanju je prišlo do napake. Poskusite znova.')
    {% else %}
    print('Rešujete kot anonimni uporabnik, zato rešitve niso shranjene.')
    {% endif %}

_check()

#####################################################################@@#
