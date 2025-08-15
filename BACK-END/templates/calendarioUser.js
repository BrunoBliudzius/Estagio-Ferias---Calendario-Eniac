document.addEventListener("DOMContentLoaded", async function () {
    let calendarEl = document.getElementById("calendar");
    
    // Faz a chamada para a nova rota que verifica o status de administrador
    const loginRes = await fetch("http://localhost:5000/check-admin-status");
    const loginStatus = await loginRes.json();
    const isAdmin = loginStatus.isAdmin; // Usa a propriedade 'isAdmin' da resposta

    let calendar = new FullCalendar.Calendar(calendarEl, {
        eventClick: function (info) {
            const event = info.event;
            idEventoSelecionado = event.id;

            document.querySelector(".modal-title").textContent = event.title;
            document.querySelector(".modal-body p:first-of-type").innerHTML =
                `<strong>Data:</strong> ${event.start.toLocaleDateString()}<br><strong>Descrição:</strong> ${event.extendedProps.descricao}`;

            // Exibe o nome do usuário que alterou o evento SOMENTE se for admin
            const usuarioEl = document.getElementById("modal-usuario");
            if (isAdmin && event.extendedProps.usuario_nome) {
                usuarioEl.innerHTML = `<strong>Última alteração por:</strong> ${event.extendedProps.usuario_nome}`;
            } else {
                usuarioEl.innerHTML = "";
            }

            if (event.extendedProps.imagem_url) {
                if (!document.getElementById("modal-img-evento")) {
                    const img = document.createElement("img");
                    img.id = "modal-img-evento";
                    img.style.maxWidth = "100%";
                    img.style.marginTop = "10px";
                    document.querySelector(".modal-body").appendChild(img);
                }
                document.getElementById("modal-img-evento").src = event.extendedProps.imagem_url;
                document.getElementById("modal-img-evento").style.display = "block";
            } else {
                if (document.getElementById("modal-img-evento")) {
                    document.getElementById("modal-img-evento").style.display = "none";
                }
            }

            document.getElementById("editNomeEvento").value = event.title;
            document.getElementById("editDataInicial").value = event.startStr;
            document.getElementById("editDataFinal").value = event.endStr
                ? new Date(new Date(event.endStr).setDate(new Date(event.endStr).getDate() - 1)).toISOString().split("T")[0]
                : event.startStr;
            document.getElementById("editCorEvento").value = event.backgroundColor || "#3788d8";
            document.getElementById("editDescricao").value = event.extendedProps.descricao || "";

            new bootstrap.Modal(document.querySelector(".modal")).show();
        },
        height: "auto",
        initialView: "dayGridMonth",
        locale: "pt-br",
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
        }
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
                usuario_nome: evt.usuario_nome || null
            }
        });
    });
});