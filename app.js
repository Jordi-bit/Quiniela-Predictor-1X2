// app.js final para quiniela 1X2 con historial dinámico y nombres oficiales de equipos
let model;
let historial = {};
let historialCargado = false;

// Lista completa de equipos con nombres oficiales según historial.json
const equipos = [
    'FC Barcelona', 'Real Madrid', 'Atlético de Madrid', 'Sevilla FC', 'Real Sociedad', 'Girona FC', 'Real Betis',
    'Villarreal CF', 'Valencia CF', 'Athletic Club', 'RC Celta', 'Rayo Vallecano', 'RCD Espanyol de Barcelona',
    'CA Osasuna', 'UD Las Palmas', 'Real Valladolid CF', 'Getafe CF', 'RCD Mallorca', 'Deportivo Alaves', 'CD Leganés',
    'ALBACETE', 'ALMERIA', 'BURGOS', 'CADIZ', 'CARTAGENA', 'CASTELLON', 'CORDOBA', 'DEPORTIVO', 'EIBAR',
    'ELCHE', 'ELDENSE', 'GRANADA', 'HUESCA', 'LEVANTE', 'MALAGA', 'MIRANDES', 'OVIEDO', 'FERROL',
    'RACING', 'SPORTING', 'TENERIFE', 'ZARAGOZA'
];

// Inicializar selects y cargar modelo e historial
window.onload = async () => {
    const selLocal = document.getElementById("local");
    const selVisitante = document.getElementById("visitante");

    equipos.sort().forEach(e => {
        const opt1 = document.createElement("option");
        opt1.value = e;
        opt1.text = e;
        selLocal.appendChild(opt1);

        const opt2 = document.createElement("option");
        opt2.value = e;
        opt2.text = e;
        selVisitante.appendChild(opt2);
    });

    // Cargar historial desde JSON
    try {
        const response = await fetch('historial.json');
        const data = await response.json();
        
        data.forEach(partido => {
            const local = partido.Equipo_Local;
            const visitante = partido.Equipo_Visitante;

            historial[local] = historial[local] || { goles: [], resultados: [] };
            historial[visitante] = historial[visitante] || { goles: [], resultados: [] };

            historial[local].goles.push(partido.Goles_Local);
            historial[local].resultados.push(partido.Resultado);

            historial[visitante].goles.push(partido.Goles_Visitante);
            historial[visitante].resultados.push(-partido.Resultado);
        });

        historialCargado = true;
        console.log("Historial cargado correctamente");
    } catch (e) {
        console.error("Error cargando historial:", e);
    }

    // Cargar modelo TensorFlow.js
    try {
        console.log("Intentando cargar modelo desde web_model/model.json...");
        model = await tf.loadLayersModel("web_model/model.json");
        console.log("✅ Modelo cargado correctamente");
    } catch (e) {
        console.error("❌ Error cargando el modelo:", e);
        document.getElementById("resultados").innerHTML = `
            <div style="color: red; padding: 10px; border: 1px solid red; border-radius: 5px;">
                <p><b>Error al cargar el modelo predictivo:</b></p>
                <p>${e.message}</p>
                <p>Esto puede deberse a que el servidor local no está entregando correctamente los archivos en <code>web_model/</code>.</p>
            </div>
        `;
    }
};

// Función para calcular features automáticas
function calcularFeatures(local, visitante) {
    const hLocal = historial[local] || { goles: [0], resultados: [0] };
    const hVisit = historial[visitante] || { goles: [0], resultados: [0] };

    const golesLocalProm = hLocal.goles.reduce((a, b) => a + b, 0) / hLocal.goles.length;
    const golesVisitProm = hVisit.goles.reduce((a, b) => a + b, 0) / hVisit.goles.length;
    const diferenciaGoles = golesLocalProm - golesVisitProm;

    const victorias = hLocal.resultados.filter(r => r === 1).length;
    const empates = hLocal.resultados.filter(r => r === 0).length;
    const derrotas = hLocal.resultados.filter(r => r === -1).length;

    const promGolesRival = 0; // Según tutorial
    const ultimoResultado = hLocal.resultados[hLocal.resultados.length - 1] || 0;
    const localFlag = 1;

    return [golesLocalProm, golesVisitProm, diferenciaGoles, victorias, empates, derrotas, promGolesRival, ultimoResultado, localFlag];
}

// Función de predicción
async function predecir() {
    if (!historialCargado) {
        alert("El historial aún no se ha cargado. Espera unos segundos.");
        return;
    }
    if (!model) {
        alert("El modelo no está cargado. Asegúrate de haberlo entrenado.");
        return;
    }

    const local = document.getElementById("local").value;
    const visitante = document.getElementById("visitante").value;

    if (local === visitante) {
        alert("Selecciona equipos diferentes.");
        return;
    }

    const features = calcularFeatures(local, visitante);
    const tensor = tf.tensor2d([features]);
    const pred = model.predict(tensor);

    const data = await pred.array();
    const [p_local, p_empate, p_visitante] = data[0];

    document.getElementById("resultados").innerHTML = `
        <h3 style="margin-top: 0">Probabilidades:</h3>
        <p>🏠 <b>Gana Local:</b> ${(p_local * 100).toFixed(2)}%</p>
        <p>➖ <b>Empate:</b> ${(p_empate * 100).toFixed(2)}%</p>
        <p>🚩 <b>Gana Visitante:</b> ${(p_visitante * 100).toFixed(2)}%</p>
        <div style="margin-top: 15px; font-weight: bold; color: #1a73e8; text-align: center;">
            Predicción: ${p_local > p_empate && p_local > p_visitante ? '1' : (p_empate > p_visitante ? 'X' : '2')}
        </div>
    `;
}
