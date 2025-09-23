document.addEventListener("DOMContentLoaded", async function () {

    let calendarEl = document.getElementById("calendar");
    
    const loginRes = await fetch("http://localhost:5000/check-admin-status");
    const loginStatus = await loginRes.json();
    const isAdmin = loginStatus.isAdmin;

    let calendar = new FullCalendar.Calendar(calendarEl, {
        eventClick: function (info) {
            const event = info.event;
        
            const viewModal = new bootstrap.Modal(document.getElementById("viewEventModal"));
        
            document.querySelector("#viewEventModal .modal-title").textContent = event.title;
            
            const startDate = event.start;
            let endDate = event.end;
            let dateString = '';
        
            let inclusiveEndDate = null;
            if (endDate) {
                inclusiveEndDate = new Date(endDate);
                inclusiveEndDate.setDate(inclusiveEndDate.getDate() - 1);
            }
        
            if (!inclusiveEndDate || startDate.toDateString() === inclusiveEndDate.toDateString()) {
                dateString = `<strong>Data:</strong> ${startDate.toLocaleDateString()}`;
            } else {
                dateString = `<strong>Data de Início:</strong> ${startDate.toLocaleDateString()}<br><strong>Data Final:</strong> ${inclusiveEndDate.toLocaleDateString()}`;
            }
            document.querySelector("#viewEventModal .modal-body .event-date").innerHTML = dateString;
        
            document.querySelector("#viewEventModal .modal-body .event-description").innerHTML = `<strong>Descrição:</strong> ${event.extendedProps.descricao || ""}`;
        
            const usuarioEl = document.getElementById("modal-usuario");
            const visibilityEl = document.querySelector("#viewEventModal .modal-body .event-visibility");
        
            if (isAdmin) {
                if (event.extendedProps.usuario_nome) {
                    usuarioEl.innerHTML = `<strong>Última alteração por:</strong> ${event.extendedProps.usuario_nome}`;
                    usuarioEl.style.display = 'block';
                } else {
                    usuarioEl.style.display = 'none';
                }
        
                if (event.extendedProps.evento_tipo) {
                    const tipos = event.extendedProps.evento_tipo.split(',').map(tipo => tipo.charAt(0).toUpperCase() + tipo.slice(1)).join(', ');
                    visibilityEl.innerHTML = `<strong>Visível para:</strong> ${tipos}`;
                    visibilityEl.style.display = 'block';
                } else {
                    visibilityEl.style.display = 'none';
                }
            } else {
                usuarioEl.style.display = 'none';
                visibilityEl.style.display = 'none';
            }
        
            const imgContainer = document.querySelector("#viewEventModal .modal-body .event-image-container");
            imgContainer.innerHTML = '';
            if (event.extendedProps.imagem_url) {
                const imgEl = document.createElement("img");
                imgEl.id = "view-modal-img-evento";
                imgEl.src = event.extendedProps.imagem_url;
                imgEl.style.maxWidth = "100%";
                imgEl.style.marginTop = "10px";
                imgContainer.appendChild(imgEl);
            }
        
            viewModal.show();
        },
        // ==========================================================
        // ALTURA DO CALENDÁRIO AJUSTADA AQUI
        // ==========================================================
        height: "100%", // Altera de 'auto' para '100%'
        initialView: "dayGridMonth",
        firstDay: 0,
        locale: "pt-br",
        weekNumbers: true,
        weekNumbersWithinDays: false,
        weekNumberContent: function(arg) {
            return { html: 'S' + arg.num };
        },        
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "customMonthPicker"
        },
        customButtons: {
            customMonthPicker: {
                text: "Selecionar mês",
                click: function () {
                    document.getElementById("monthPicker").showPicker();
                }
            }
        },
    });

    calendar.render();

    let monthInput = document.createElement("input");
    monthInput.type = "month";
    monthInput.id = "monthPicker";
    monthInput.className = "form-control form-control-sm";
    monthInput.style.display = "inline-block";
    monthInput.style.width = "150px";
    monthInput.style.marginLeft = "10px";

    monthInput.addEventListener("change", function () {
        if (this.value) {
            calendar.gotoDate(this.value + "-01");
        }
    });

    document.querySelector(".fc-toolbar-chunk:last-child").appendChild(monthInput);

    const res = await fetch("http://localhost:5000/datas");
    const eventos = await res.json();
    eventos.forEach(evt => {
        let dataFinal = new Date(evt.dataFinal);
        dataFinal.setDate(dataFinal.getDate() + 1);
        calendar.addEvent({
            id: evt.id,
            title: evt.nomeEvento,
            start: evt.dataInicial,
            end: dataFinal.toISOString().split("T")[0],
            color: evt.eventColor || "#3788d8",
            extendedProps: {
                descricao: evt.descricao || "",
                imagem_url: evt.imagem_url || null,
                usuario_nome: evt.usuario_nome || null,
                evento_tipo: evt.evento_tipo || 'externo'
            }
        });
    });
});