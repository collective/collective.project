Changelog
=========

2.0.0 (2015-07-05)
------------------

- Plone 5 compat

1.0.1 (2012-10-29)
------------------

- Add 4.3 compat
- Add classifers to setup.py for all Plone 4.x

1.0.0 (2012-04-07)
------------------

- Clean up package

0.9.5 (08/17/2011)
------------------

- Do not hide Plone content editing border by default
- Change default projects
- Clean up UI
- More package cleanup

0.9.4 (11/10/2010)
------------------

- Clean up package
- Rebrand as demo application

0.9.3 (12/05/2009)
------------------

- Fix bug with calculation of hours when exactly a full day (24 hours) has been worked
- Rename class method iteration_tool (in CreateIterationForm) to create_iteration
- Add class method to CreateIterationForm (deactivate_iteration) to change workflow state on all active iterations (to inactive) when creating new iterations
- UI enhancements to project, iteration, task templates
- Factor out some class methods into common.py
- Improved client view template
- Add additional fields to client type

0.9.2 (11/30/2009)
------------------

- Provide improved installation instructions in INSTALL.txt

0.9.1 (11/19/2009)
------------------

- Iteration tool bug fixes 
- Date range tweaks on projects, iterations 
- Add drop down menu to select Project title, powered by portal property and SimpleVocabulary
- Add portal property to make disable border configurable on all types

0.9.0 (11/17/2009)
------------------

- Restore iteration tool

0.8.0 (10/08/2009)
------------------

- Fix hours calculation for increments of time < 1 hour
- Calculate totals for active iterations only
- Don't show inactive iterations in iteration_templates/view.pt
- Change defaults for start and stop of projects & iterations

0.7.0 (09/29/2009)
------------------

- Package shipped without top level docs directory, fixed
- projects_view was broken in several ways, fixed

0.6.0 (09/25/2009)
------------------

- Rename package to 'collective.project'
- Final Dexterity content types implementation
- Provides custom view templates for Project, Iteration, and Task as well as three top level views

0.5.0 (08/16/2009)
------------------

- Initial Dexterity content types implementation

0.4.0 (08/14/2009)
------------------

- Track variable and flat rate fee projects (e.g. consulting and hosting)
- Compute totals for active projects only

0.3.0 (03/19/2009)
------------------

- Bug fix in iteration_view template

0.2.0 (03/19/2009)
------------------

- Add billable field to task
- Add sort_on = getObjPositionInParent to projects_view to display projects in order

0.1.0 (03/15/2009)
------------------

- Initial release
