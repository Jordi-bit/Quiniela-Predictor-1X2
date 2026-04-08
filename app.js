// app.js final para quiniela 1X2 con historial dinámico y nombres oficiales de equipos
let model;
let statsEquipos = {}; // Aquí guardaremos las estadísticas procesadas
let historialCargado = false;

// Inicializar selects y cargar modelo e historial
window.onload = async () => {
    // Cargar historial desde JSON
    try {
        console.log("Cargando historial.json...");
        const response = await fetch("historial.json");
        if (!response.ok) throw new Error("No se pudo cargar historial.json");
        
        const data = await response.json();
        const partidos = data.partidos;
        
        // Procesar partidos para generar estadísticas por equipo
        partidos.forEach(partido => {
            const local = partido.Equipo_Local;
            const visitante = partido.Equipo_Visitante;

            if (!statsEquipos[local]) statsEquipos[local] = { goles: [], resultados: [] };
            if (!statsEquipos[visitante]) statsEquipos[visitante] = { goles: [], resultados: [] };

            statsEquipos[local].goles.push(partido.Goles_Local);
            statsEquipos[local].resultados.push(partido.Resultado);

            statsEquipos[visitante].goles.push(partido.Goles_Visitante);
            statsEquipos[visitante].resultados.push(-partido.Resultado);
        });

        // Cargar SOLO los equipos actuales en los select
        const selLocal = document.getElementById("local");
        const selVisitante = document.getElementById("visitante");
        
        data.equipos_actuales.forEach(equipo => {
            const opt1 = document.createElement("option");
            opt1.value = equipo;
            opt1.text = equipo;
            selLocal.appendChild(opt1);

            const opt2 = document.createElement("option");
            opt2.value = equipo;
            opt2.text = equipo;
            selVisitante.appendChild(opt2);
        });
        
        historialCargado = true;
        console.log(`✅ ${partidos.length} partidos procesados. ${data.equipos_actuales.length} equipos listos.`);
    } catch (e) {
        console.error("❌ Error cargando el historial:", e);
        document.getElementById("resultados").innerHTML = `<p style="color:red">Error: ${e.message}</p>`;
    }

    // Cargar modelo TensorFlow.js
    try {
        console.log("Cargando modelo...");
        model = await tf.loadLayersModel("web_model/model.json");
        console.log("✅ Modelo cargado correctamente");
    } catch (e) {
        console.error("❌ Error cargando el modelo:", e);
        document.getElementById("resultados").innerHTML = `<p style="color:red">Error cargando modelo: ${e.message}</p>`;
    }
};

// Función para calcular features automáticas basándose en TODA la historia procesada
function calcularFeatures(local, visitante) {
    const sLocal = statsEquipos[local] || { goles: [0], resultados: [0] };
    const sVisit = statsEquipos[visitante] || { goles: [0], resultados: [0] };

    const golesLocalProm = sLocal.goles.reduce((a, b) => a + b, 0) / Math.max(1, sLocal.goles.length);
    const golesVisitProm = sVisit.goles.reduce((a, b) => a + b, 0) / Math.max(1, sVisit.goles.length);
    const diferenciaGoles = golesLocalProm - golesVisitProm;

    const victorias = sLocal.resultados.filter(r => r === 1).length;
    const empates = sLocal.resultados.filter(r => r === 0).length;
    const derrotas = sLocal.resultados.filter(r => r === -1).length;

    const vVictorias = sVisit.resultados.filter(r => r === 1).length;
    const vEmpates = sVisit.resultados.filter(r => r === 0).length;
    const vDerrotas = sVisit.resultados.filter(r => r === -1).length;

    const promGolesRival = golesVisitProm; 
    const ultimoResultado = sLocal.resultados[sLocal.resultados.length - 1] || 0;
    const localFlag = 1;

    // El modelo espera 9 features
    return [
        golesLocalProm, golesVisitProm, diferenciaGoles, 
        victorias, empates, derrotas, 
        vVictorias, vEmpates, vDerrotas
    ];
}

// Función de predicción
async function predecir() {
    if (!historialCargado || !model) {
        alert("El sistema aún se está cargando. Por favor, espera.");
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
        <h3 style="margin-top: 0; color: #3b82f6;">Probabilidades:</h3>
        <p>🏠 <b>Gana Local:</b> ${(p_local * 100).toFixed(2)}%</p>
        <p>➖ <b>Empate:</b> ${(p_empate * 100).toFixed(2)}%</p>
        <p>🚩 <b>Gana Visitante:</b> ${(p_visitante * 100).toFixed(2)}%</p>
        <div style="margin-top: 15px; font-weight: bold; color: #3b82f6; text-align: center; font-size: 1.2em; border-top: 1px solid #444; pt: 10px;">
            Predicción Recomendada: ${p_local > p_empate && p_local > p_visitante ? '1' : (p_empate > p_visitante ? 'X' : '2')}
        </div>
    `;
}
