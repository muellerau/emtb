##################################
##
## ChimeraX extension
## Adds command 'arrangegrid' to
## arrange models in a grid.
##
## (c)2021 - Andreas U. Mueller
##
##      use at own risk
##
##################################

def arrange_grid(session, models, ag_columns=0, ag_distance=200):
    from chimerax.core.commands import run
    import math
    if ag_columns==0 or not ag_columns: ag_columns=len(models)
    for model in models:
        md_num=models.index(model)
        md_row=math.floor(md_num/ag_columns)
        md_rcol=md_num-(ag_columns*md_row)
        run(session, 'move 1,0,0 %s models #%s' % (ag_distance*md_rcol, model.id_string)) # move column
        run(session, 'move 0,1,0 %s models #%s' % (ag_distance*-1*md_row, model.id_string)) # move row
    run(session, 'view')

def register_command(session):
    from chimerax.core.commands import CmdDesc, register, IntArg
    from chimerax.core.commands import SurfacesArg
    desc = CmdDesc(required=[('models', SurfacesArg)], optional=[('ag_columns', IntArg), ('ag_distance', IntArg)],
                   synopsis='Arrange models in a grid; usage: arrangegrid modelSpec columns distance')
    register('arrangegrid', desc, arrange_grid, logger=session.logger)

register_command(session)