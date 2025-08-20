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

            // Agora, sempre abra o modal de visualização
            const viewModal = new bootstrap.Modal(document.getElementById("viewEventModal")); // APONTE PARA O ID DO SEU MODAL DE VISUALIZAÇÃO

            // Preencha os campos do modal de visualização
            document.querySelector("#viewEventModal .modal-title").textContent = event.title;
            document.querySelector("#viewEventModal .modal-body .event-date").innerHTML = `<strong>Data:</strong> ${event.start.toLocaleDateString()}`;
            document.querySelector("#viewEventModal .modal-body .event-description").innerHTML = `<strong>Descrição:</strong> ${event.extendedProps.descricao}`;

            // Lógica para imagem
            const imgContainer = document.querySelector("#viewEventModal .modal-body .event-image-container");
            if (event.extendedProps.imagem_url) {
                let imgEl = document.getElementById("view-modal-img-evento");
                if (!imgEl) {
                    // Crie a tag img se ela ainda não existir
                    imgEl = document.createElement("img");
                    imgEl.id = "view-modal-img-evento";
                    imgEl.style.maxWidth = "100%";
                    imgEl.style.marginTop = "10px";
                    imgContainer.appendChild(imgEl);
                }
                imgEl.src = event.extendedProps.imagem_url;
                imgEl.style.display = "block"; // Garante que a imagem é visível
            } else {
                // Se não houver imagem, esconda o elemento img se ele existir
                const imgEl = document.getElementById("view-modal-img-evento");
                if (imgEl) {
                    imgEl.style.display = "none";
                }
            }


            // Exibe o nome do usuário que alterou o evento SOMENTE se for admin
            const usuarioEl = document.getElementById("modal-usuario");
            if (isAdmin && event.extendedProps.usuario_nome) {
                usuarioEl.innerHTML = `<strong>Última alteração por:</strong> ${event.extendedProps.usuario_nome}`;
            } else {
                usuarioEl.innerHTML = "";
            }

            viewModal.show(); // Exibe o modal
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