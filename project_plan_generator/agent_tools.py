async def gather_project_details(ctx):
    return {
        "name": ctx.deps.project_name,
        "objectives": ctx.deps.objectives,
        "timeline": ctx.deps.timeline,
        "team_size": ctx.deps.team_size,
        "key_features": ctx.deps.key_features,
    }

async def generate_project_plan(project_details):
    # In a real scenario, this might call an LLM or use a template system
    # For now, we'll create a more comprehensive project plan structure
    team_size = project_details['team_size']
    
    # Calculate resources based on team size
    developers = max(1, int(team_size * 0.6))
    testers = max(1, int(team_size * 0.2))
    designers = max(1, int(team_size * 0.1))
    project_managers = max(1, int(team_size * 0.1))
    
    # Create a more detailed plan
    return {
        "phases": [
            "Initiation",
            "Planning",
            "Design",
            "Development",
            "Testing",
            "Deployment",
            "Maintenance"
        ],
        "milestones": [
            "Project Charter Approved",
            "Requirements Specification Completed",
            "Design Documents Approved",
            "Alpha Version Released",
            "Beta Testing Completed",
            "Version 1.0 Released",
            "First Maintenance Update"
        ],
        "tasks": [
            "Define project scope and objectives",
            "Identify stakeholders and gather requirements",
            "Create project schedule and resource plan",
            "Design system architecture",
            "Create detailed technical specifications",
            "Set up development environment",
            "Implement core features",
            "Develop user interface",
            "Perform unit testing",
            "Conduct integration testing",
            "Execute user acceptance testing",
            "Prepare deployment documentation",
            "Train end users",
            "Deploy to production",
            "Monitor system performance",
            "Gather user feedback",
            "Plan for future enhancements"
        ],
        "resource_allocation": {
            "developers": developers,
            "testers": testers,
            "designers": designers,
            "project_managers": project_managers
        }
    }

# Placeholder for future tool functions if needed
# Currently, no specific tools have been defined for the financial tracker agent.
