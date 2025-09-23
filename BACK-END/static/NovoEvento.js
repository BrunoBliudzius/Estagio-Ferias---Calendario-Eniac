let idEventoSelecionado = null;
let calendar;
let monthInput = null;

document.addEventListener("DOMContentLoaded", async function () {
    let calendarEl = document.getElementById("calendar");

    calendar = new FullCalendar.Calendar(calendarEl, {
        eventClick: function (info) {
            const event = info.event;
            idEventoSelecionado = event.id;

            document.querySelector(".modal-title").textContent = event.title;
            
            const startDate = event.start;
            const endDate = event.end;
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
            
            document.querySelector(".modal-body p:first-of-type").innerHTML = `${dateString}<br><strong>Descrição:</strong> ${event.extendedProps.descricao}`;
            
            const usuarioEl = document.getElementById("modal-usuario");
            if (event.extendedProps.usuario_nome) {
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
            document.getElementById("editDataFinal").value = inclusiveEndDate.toISOString().split("T")[0];
            document.getElementById("editCorEvento").value = event.backgroundColor || "#3788d8";
            document.getElementById("editDescricao").value = event.extendedProps.descricao || "";
            
            const tiposVisiveis = (event.extendedProps.evento_tipo || '').split(',');
            document.getElementById('edit_tipo_aluno').checked = tiposVisiveis.includes('aluno');
            document.getElementById('edit_tipo_externo').checked = tiposVisiveis.includes('externo');
            document.getElementById('edit_tipo_admin').checked = tiposVisiveis.includes('admin');

            const imgContainer = document.getElementById("editImagemEvento").parentElement;
            let imgPreview = document.getElementById("editImagemPreview");
            if (!imgPreview) {
                imgPreview = document.createElement("img");
                imgPreview.id = "editImagemPreview";
                imgPreview.style.maxWidth = "100%";
                imgPreview.style.marginTop = "10px";
                imgContainer.appendChild(imgPreview);
            }
            imgPreview.src = event.extendedProps.imagem_url || "";

            new bootstrap.Modal(document.querySelector(".modal")).show();
        },
        // ==========================================================
        // ALTURA DO CALENDÁRIO AJUSTADA AQUI
        // ==========================================================
        height: 1170, // Altere este valor em pixels conforme desejado
        initialView: "dayGridMonth",
        locale: "pt-br",
        weekNumbers: true,
        weekNumbersWithinDays: false,
        weekNumberContent: function (arg) {
            return { html: 'S' + arg.num };
        },
        datesSet: function () {
            if (!monthInput) return;
            const d = calendar.getDate();
            const ym = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0");
            monthInput.value = ym;
        }
    });

    calendar.render();

    const wrapper = document.createElement("div");
    wrapper.className = "d-inline-flex align-items-center ms-2";

    monthInput = document.createElement("input");
    monthInput.type = "month";
    monthInput.className = "form-control form-control-sm";
    monthInput.style.width = "170px";

    const cur = calendar.getDate();
    monthInput.value = cur.getFullYear() + "-" + String(cur.getMonth() + 1).padStart(2, "0");

    function gotoMonth() {
        if (monthInput.value) {
            calendar.gotoDate(monthInput.value + "-01");
        }
    }
    monthInput.addEventListener("change", gotoMonth);

    const rightChunk =
        calendarEl.querySelector(".fc-header-toolbar .fc-toolbar-chunk:last-child") ||
        calendarEl.querySelector(".fc-header-toolbar .fc-toolbar-chunk");
    wrapper.appendChild(monthInput);
    if (rightChunk) rightChunk.appendChild(wrapper);

    const res = await fetch("http://localhost:5000/datas");
    const eventos = await res.json();
    eventos.forEach((evt) => {
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
                evento_tipo: evt.evento_tipo || ''
            },
        });
    });
});

const dataInicialInput = document.getElementById("DataEvento");
const dataFinalInput = document.getElementById("DataEvento2");

dataInicialInput.addEventListener("change", function () {
    dataFinalInput.min = this.value;
    if (dataFinalInput.value < this.value) {
        dataFinalInput.value = this.value;
    }
});

const editDataInicialInput = document.getElementById("editDataInicial");
const editDataFinalInput = document.getElementById("editDataFinal");

editDataInicialInput.addEventListener("change", function () {
    editDataFinalInput.min = this.value;
    if (editDataFinalInput.value < this.value) {
        editDataFinalInput.value = this.value;
    }
});

document.getElementById("modalEditarEvento").addEventListener("show.bs.modal", function () {
    if (editDataInicialInput.value) {
        editDataFinalInput.min = editDataInicialInput.value;
    }
});

document.getElementById("formEvento").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(document.getElementById("formEvento"));

    const nomeEvento = formData.get("nomeEvento").trim();
    if (nomeEvento.length < 3) {
        alert("O nome do evento deve ter pelo menos 3 caracteres.");
        return;
    }

    const res = await fetch("http://localhost:5000/datas", {
        method: "POST",
        body: formData,
    });

    if (res.ok || res.status === 201) {
        location.reload();
    } else {
        try {
            const errorData = await res.json();
            if (errorData && errorData.erro) {
                alert(errorData.erro);
            } else {
                alert("Erro ao cadastrar evento!");
            }
        } catch (error) {
            alert("Ocorreu um erro inesperado ao cadastrar o evento.");
        }
    }
});

async function FuncaoPesquisa() {
    const pesquisa = document.getElementById("pesquisa").value.trim();

    if (!pesquisa) {
        alert("Por favor, digite um termo para pesquisar.");
        return;
    }

    const res = await fetch(
        `http://localhost:5000/datasFiltro?nomeEvento=${pesquisa}`
    );
    const eventos = await res.json();
    const tbody = document.getElementById("tbodyEventos");
    tbody.innerHTML = "";
    eventos.forEach((evt) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${evt.id}</td>
            <td>${evt.nomeEvento}</td>
            <td>${evt.dataInicial.split("T")[0]}</td>
            <td>${evt.dataFinal.split("T")[0]}</td>
            <td style="background:${evt.eventColor}"></td>
            <td><button class="btn btn-primary btn-sm" onclick='abrirModalEvento(${JSON.stringify(evt)})'>Ver</button></td>
        `;
        tbody.appendChild(row);
    });
}

function abrirModalEvento(evt) {
    const evento = evt.event || evt;
    idEventoSelecionado = evento.id;

    document.querySelector(".modal-title").textContent = evento.title || evento.nomeEvento;
    
    const startDate = new Date(evento.start || evento.dataInicial);
    const endDate = new Date(evento.endStr ? new Date(evento.endStr).setDate(new Date(evento.endStr).getDate() - 1) : (evento.dataFinal || evento.start || evento.dataInicial));
    let dateString = '';

    if (startDate.toDateString() === endDate.toDateString()) {
        dateString = `<strong>Data:</strong> ${startDate.toLocaleDateString()}`;
    } else {
        dateString = `<strong>Data de Início:</strong> ${startDate.toLocaleDateString()}<br><strong>Data Final:</strong> ${endDate.toLocaleDateString()}`;
    }

    document.querySelector(".modal-body p:first-of-type").innerHTML = `${dateString}<br><strong>Descrição:</strong> ${evento.extendedProps?.descricao || evt.descricao || ""}`;

    const usuarioEl = document.getElementById("modal-usuario");
    if (usuarioEl) {
        const usuarioNome = evento.extendedProps?.usuario_nome || evt.usuario_nome;
        if (usuarioNome) {
            usuarioEl.innerHTML = `<strong>Última alteração por:</strong> ${usuarioNome}`;
        } else {
            usuarioEl.innerHTML = "";
        }
    }

    let modalImg = document.getElementById("modal-img-evento");
    const imagemUrl = evento.extendedProps?.imagem_url || evt.imagem_url;
    if (imagemUrl) {
        if (!modalImg) {
            modalImg = document.createElement("img");
            modalImg.id = "modal-img-evento";
            modalImg.style.maxWidth = "100%";
            modalImg.style.marginTop = "10px";
            document.querySelector(".modal-body").appendChild(modalImg);
        }
        modalImg.src = imagemUrl;
        modalImg.style.display = "block";
    } else if (modalImg) {
        modalImg.style.display = "none";
    }
    
    document.getElementById("editNomeEvento").value = evento.title || evt.nomeEvento;
    document.getElementById("editDataInicial").value = (evento.startStr || evt.dataInicial).split("T")[0];
    document.getElementById("editDataFinal").value = (evt.dataFinal || endDate.toISOString()).split("T")[0];
    document.getElementById("editCorEvento").value = evento.backgroundColor || evt.eventColor || "#3788d8";
    document.getElementById("editDescricao").value = evento.extendedProps?.descricao || evt.descricao || "";

    const tiposVisiveis = (evento.extendedProps?.evento_tipo || evt.evento_tipo || '').split(',');
    document.getElementById('edit_tipo_aluno').checked = tiposVisiveis.includes('aluno');
    document.getElementById('edit_tipo_externo').checked = tiposVisiveis.includes('externo');
    document.getElementById('edit_tipo_admin').checked = tiposVisiveis.includes('admin');

    const imgContainer = document.getElementById("editImagemEvento").parentElement;
    let imgPreview = document.getElementById("editImagemPreview");
    if (!imgPreview) {
        imgPreview = document.createElement("img");
        imgPreview.id = "editImagemPreview";
        imgPreview.style.maxWidth = "100%";
        imgPreview.style.marginTop = "10px";
        imgContainer.appendChild(imgPreview);
    }
    imgPreview.src = imagemUrl || "";

    const eventModal = new bootstrap.Modal(document.querySelector('.modal'));
    eventModal.show();
}

async function FuncaoDeletar() {
    if (!idEventoSelecionado) {
        alert("Nenhum evento selecionado!");
        return;
    }
    const res = await fetch(
        `http://localhost:5000/datas/${idEventoSelecionado}`,
        {
            method: "DELETE",
        }
    );
    if (res.ok) {
        alert("Evento deletado com sucesso!");
        location.reload();
    } else {
        alert("Erro ao deletar evento.");
    }
}

function FuncaoAtualizar() {
    const viewModal = bootstrap.Modal.getInstance(document.querySelector('.modal'));
    if (viewModal) viewModal.hide();
    
    const modalEdicao = new bootstrap.Modal(
        document.getElementById("modalEditarEvento")
    );
    modalEdicao.show();
}

document
    .getElementById("formEditarEvento")
    .addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("nomeEvento", document.getElementById("editNomeEvento").value.trim());
        formData.append("dataInicial", document.getElementById("editDataInicial").value);
        formData.append("dataFinal", document.getElementById("editDataFinal").value);
        formData.append("descricao", document.getElementById("editDescricao").value.trim());
        formData.append("eventColor", document.getElementById("editCorEvento").value);

        document.querySelectorAll('#modalEditarEvento input[name="evento_tipo"]:checked').forEach(checkbox => {
            formData.append('evento_tipo', checkbox.value);
        });

        const imagemFile =
            document.getElementById("editImagemEvento").files[0];
        if (imagemFile) {
            formData.append("imagem", imagemFile);
        }

        const res = await fetch(
            `http://localhost:5000/datas/${idEventoSelecionado}`,
            {
                method: "PUT",
                body: formData,
            }
        );

        if (res.ok) {
            alert("Evento atualizado com sucesso!");
            location.reload();
        } else {
            try {
                const errorData = await res.json();
                if (errorData && errorData.erro) {
                    alert(errorData.erro);
                } else {
                    alert("Erro ao atualizar evento.");
                }
            } catch (error) {
                alert("Ocorreu um erro inesperado ao atualizar o evento.");
            }
        }
    });