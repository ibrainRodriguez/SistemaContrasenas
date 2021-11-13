function modoUso() {
    echo "-----------------------------------------------"
    echo "|                Modo Uso                     |"
    echo "|                                             |"
    echo "|        Arranca el proyecto Django           |"
    echo "|                                             |"
    echo "|           ./run.sh archivo.env              |"
    echo "-----------------------------------------------"
}

function validar(){
    [[ "$1" ]] || { echo "Necesitas Selecionar un archivo.env cifrando"; modoUso; exit 1; }
    [[ -f "$1" ]] || { echo "El parametro 1 debe ser un archivo valido y cifrado"; modoUso; exit 1; }
}

validar "$@"

for linea in $(ccdecrypt -c "$1"); do
    export $linea
done

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver