$(document).ready(function () {
    $('#spin_load_database').html("<div style=\"position: absolute;top: 150%;left: 50%;transform: translate(-50%, -50%);height: 110px;\">\n" +
        "<span class=\"spinner-border spinner-border-xs\" role=\"status\" aria-hidden=\"true\" style=\"width: 2rem;height: 2rem;\"></span>\n" +
        "</div>");
    const table_database = document.getElementById('table_database');
    table_database.style.filter = "blur(5px)";
    $.ajax({
        url: '/api/database',
        type: "get",
        success: (response) => {
            datatable = $('#table_database').DataTable({
                lengthMenu: [],
                pageLength: 7,
                retrieve: true,
                data: response.data,
                columns: [
                    {title: "№", data: "id"},
                    {title: "LaTeX", data: "latex"},
                    {title: "Дата создания", data: "created_at"},
                ],
                language: {
                    lengthMenu: "",
                    search: "Поиск:",
                    searchPlaceholder: "Поиск...",
                    info: "Формулы с _START_ по _END_ из _TOTAL_",
                    infoEmpty: "",
                    infoFiltered: "",
                    zeroRecords: "Формулы не найдены",
                    emptyTable: "Формулы не найдены",
                    paginate: {
                        next: '<i class="mdi mdi-arrow-right"></i>',
                        previous: '<i class="mdi mdi-arrow-left"></i>'
                    }
                },
                dom: '<"row"<"col-md-6"<"float-left"B>><"col-md-6"f>>rt<"row"<"col-md-6"i><"col-md-6"p>>',
                buttons: [
                    'excel'
                ],
                initComplete: function () {
                    $('div.dataTables_wrapper div.dataTables_filter input').removeClass('form-control-sm')
                    $('div.dataTables_wrapper div.dataTables_filter input').addClass('form-control-lg')
                    $('div.dataTables_wrapper div.dataTables_filter label').addClass('mb-0')
                }
            });

            var math = document.getElementsByClassName('math');
            for (var i = 0; i < math.length; i++) {
                katex.render(math[i].textContent, math[i], {
                    throwOnError: false,
                    macros: {
                        "\\addBar": "\\bar{#1}",
                        "\\bold": "\\mathbf{#1}",
                        "\\f": "#1f(#2)"
                    }
                });
            }

            // Удаление кружка загрузки и блюра
            $('#spin_load_database').html("");
            table_database.style.filter = null;
        },
        error: function (xhr, status, error) {
            console.error('Произошла ошибка:', error);
        }
    });
});