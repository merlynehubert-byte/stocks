# Cursor Background Agent Configuration

This directory contains the configuration files for your Cursor background agent, which will continuously work on improving your stock analysis application.

## Files Overview

### `settings.json`
Main configuration file that enables the background agent and defines basic settings.

### `environment.json`
Defines the repository and project environment settings.

### `background-tasks.json`
Detailed task definitions for what the background agent should work on.

### `background-agent-prompt.md`
The AI prompt that guides the background agent's behavior and decision-making.

### `agent-config.json`
Comprehensive configuration including permissions, workflow, and quality gates.

## How the Background Agent Works

### 1. **Continuous Monitoring**
The agent continuously scans your codebase for:
- Code quality issues
- Potential bugs
- Performance optimizations
- Security vulnerabilities
- Documentation improvements

### 2. **Task Categories**

#### Code Improvement
- Refactor complex functions
- Improve variable naming
- Add type hints
- Optimize imports
- Remove unused code

#### Bug Fixes
- Scan for errors
- Fix syntax errors
- Handle exceptions
- Validate data inputs
- Check edge cases

#### Documentation
- Update function docs
- Improve README files
- Add code comments
- Create API documentation
- Update installation instructions

#### Performance Optimization
- Optimize data processing
- Improve memory usage
- Reduce load times
- Optimize database queries
- Cache frequently used data

#### Security Audit
- Check dependency vulnerabilities
- Validate user inputs
- Secure API endpoints
- Audit file permissions
- Check for security issues

#### Test Coverage
- Add unit tests
- Create integration tests
- Improve test coverage
- Add edge case tests
- Create mock data

### 3. **Project-Specific Tasks**

#### Streamlit Optimization
- Optimize page load speed
- Improve UI responsiveness
- Add loading states
- Optimize chart rendering
- Improve navigation

#### Stock Analysis Features
- Add new technical indicators
- Improve chart visualizations
- Add more stock data sources
- Enhance analysis algorithms
- Add portfolio tracking

## Agent Permissions

The background agent has the following permissions:
- ✅ **Read/Write**: Python files, Markdown files, text files
- ✅ **Create**: New Python files, documentation, test files
- ✅ **Commit**: Can commit changes to Git
- ❌ **Push**: Cannot push directly (requires review)
- ❌ **Deploy**: Cannot deploy or install dependencies

## Quality Gates

The agent follows these quality standards:
- **Code Quality**: Low complexity, type hints, docstrings
- **Testing**: Minimum 70% test coverage
- **Security**: Vulnerability scanning, input validation
- **Documentation**: Comprehensive documentation required

## Communication

The agent will:
- Provide clear explanations for all changes
- Include examples and reasoning
- Focus on practical improvements
- Maintain professional communication
- Consider the educational nature of your application

## Monitoring and Control

### View Agent Activity
- Check the Cursor chat for agent messages
- Review Git commits made by the agent
- Monitor file changes in your editor

### Control Agent Behavior
- Modify `.cursor/settings.json` to enable/disable specific tasks
- Update `background-tasks.json` to change task priorities
- Edit `agent-config.json` to adjust permissions and workflow

### Review Process
- The agent will commit changes daily
- All changes require your review before merging
- You can approve, modify, or reject agent suggestions

## Best Practices

1. **Regular Reviews**: Check agent commits regularly
2. **Clear Communication**: Provide feedback on agent suggestions
3. **Iterative Improvement**: Let the agent learn from your preferences
4. **Security First**: Review security-related changes carefully
5. **Educational Focus**: Ensure changes maintain educational value

## Troubleshooting

### Agent Not Working
- Check that `backgroundAgent.enabled` is `true` in `settings.json`
- Verify your repository is properly connected to GitHub
- Ensure all configuration files are committed and pushed

### Too Many Changes
- Adjust task frequencies in `background-tasks.json`
- Modify commit frequency in `agent-config.json`
- Disable specific tasks that are too aggressive

### Quality Issues
- Review and adjust quality gates in `agent-config.json`
- Update the agent prompt in `background-agent-prompt.md`
- Provide feedback to improve agent behavior

## Getting Started

1. **Initial Setup**: ✅ Complete (all files created)
2. **Agent Activation**: ✅ Complete (enabled in settings)
3. **First Scan**: The agent will begin scanning your codebase
4. **First Commit**: Expect the first agent commit within 24 hours
5. **Review Process**: Review and approve agent suggestions

Your background agent is now ready to help improve your stock analysis application continuously! 