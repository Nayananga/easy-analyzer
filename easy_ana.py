from h2o_wave import main, app, Q, ui, data

from data_processor import read_data, generate_plot_data


@app('/easy_ana')
async def serve(q: Q):
    q.page.drop()

    if q.client.initialized:

        file_data = q.client.data if q.client.data else None

        if 'file_upload' in q.args:
            file_data = read_data(q.args.file_upload)
            q.client.data = file_data
        elif 'draw' in q.args:
            plot_data = generate_plot_data(file_data, q.args.x_axis, q.args.y_axis)

            v = q.page.add('content', ui.plot_card(
                box=ui.boxes('content'),
                title=q.args.title,
                data=data('group x y'),
                plot=ui.plot([ui.mark(type='line', x='=x', x_scale='linear', y='=y', y_scale='linear', color='=group',
                                      x_title=q.args.x_axis)])
            ))

            v.data = plot_data

        q.page['meta_1'] = ui.meta_card(box='', layouts=[
            ui.layout(
                # If the viewport width >= 0:
                breakpoint='xs',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for content
                    ui.zone('body', direction=ui.ZoneDirection.COLUMN, zones=[
                        # Use remaining space for content
                        ui.zone('content'),
                        # wide sidebar
                        ui.zone('sidebar', size='300px'),
                    ]),
                    ui.zone('footer'),
                ]
            ),
            ui.layout(
                # If the viewport width >= 768:
                breakpoint='m',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for body
                    ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                        # 250px wide sidebar
                        ui.zone('sidebar', size='250px'),
                        # Use remaining space for content
                        ui.zone('content'),
                    ]),
                    ui.zone('footer'),
                ]
            ),
            ui.layout(
                # If the viewport width >= 1200:
                breakpoint='xl',
                width='1200px',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for body
                    ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                        # 300px wide sidebar
                        ui.zone('sidebar', size='300px'),
                        # Use remaining space for other widgets
                        ui.zone('content'),
                    ]),
                    ui.zone('footer'),
                ]
            )
        ])

        q.page['controls'] = ui.form_card(box=ui.boxes('sidebar'), items=[
            ui.message_bar(type='success', text=f"Great! your file uploaded successfully!"),
            ui.separator(),
            ui.dropdown(name='x_axis', label='Pick your X axis', choices=[
                ui.choice(name=x, label=x) for x in file_data
            ]),
            ui.separator(),
            ui.dropdown(name='y_axis', label='Pick your Y axis', values=[], choices=[
                ui.choice(name=y, label=y) for y in file_data
            ]),
            ui.separator(),
            ui.textbox(name='title', label='Enter your plot title'),
            ui.separator(),
            ui.button(name='draw', label='Draw', primary=True),
        ])

    else:
        q.page['meta_2'] = ui.meta_card(box='', layouts=[
            ui.layout(
                # If the viewport width >= 0:
                breakpoint='xs',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for content and footer
                    ui.zone('content'),
                    ui.zone('footer'),
                ]
            ),
            ui.layout(
                # If the viewport width >= 768:
                breakpoint='m',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for body
                    ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                        # Use remaining space for content
                        ui.zone('content'),
                    ]),
                    ui.zone('footer'),
                ]
            ),
            ui.layout(
                # If the viewport width >= 1200:
                breakpoint='xl',
                width='1200px',
                zones=[
                    # 80px high header
                    ui.zone('header', size='80px'),
                    # Use remaining space for body
                    ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                        # Use remaining space for other widgets
                        ui.zone('content'),
                    ]),
                    ui.zone('footer'),
                ]
            )
        ])

        q.page['upload'] = ui.form_card(
            box=ui.boxes('content'),
            items=[
                ui.text_xl(content='Let\'s upload your data first.'),
                ui.file_upload(name='file_upload', label='Upload!', multiple=True,
                               file_extensions=['csv', 'gz'], max_file_size=10, max_size=15)
            ]
        )

        q.client.initialized = True

    q.page['header'] = ui.header_card(
        # Place card in the header zone, regardless of viewport size.
        box='header',
        title='Easy Analyzer',
        subtitle='Show graphs instantly',
    )

    q.page['footer'] = ui.footer_card(box='footer', caption='Made with ❤️ by Nayananga ')

    await q.page.save()
