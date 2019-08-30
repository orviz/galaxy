import axios from "axios";
import { getGalaxyInstance } from "app";

/** Workflow data request helper **/
export class Services {
    constructor(options = {}) {
        this.root = options.root;
    }

    copyWorkflow(workflow) {
        const Galaxy = getGalaxyInstance();
        const url = `${this.root}api/workflows/${workflow.id}/download`;
        return new Promise((resolve, reject) => {
            axios
                .get(url)
                .then(response => {
                    let newWorkflow = response.data;
                    let newName = `Copy of ${workflow.name}`;
                    const currentOwner = workflow.owner;
                    if (currentOwner != Galaxy.user.attributes.username) {
                        newName += ` shared by user ${currentOwner}`;
                    }
                    newWorkflow.name = newName;
                    this.createWorkflow(newWorkflow)
                        .then(workflow => {
                            this._addAttributes(workflow);
                            resolve(workflow);
                        })
                        .catch(message => {
                            reject(message);
                        });
                })
                .catch(e => {
                    reject(this._errorMessage(e));
                });
        });
    }

    createWorkflow(workflow) {
        return new Promise((resolve, reject) => {
            axios
                .post(`${this.root}api/workflows`, { workflow: workflow })
                .then(response => {
                    resolve(response.data);
                })
                .catch(e => {
                    reject(this._errorMessage(e));
                });
        });
    }

    deleteWorkflow(id) {
        return new Promise((resolve, reject) => {
            axios
                .delete(`${this.root}api/workflows/${id}`)
                .then(response => {
                    resolve(response.data);
                })
                .catch(e => {
                    reject(this._errorMessage(e));
                });
        });
    }

    getWorkflows() {
        return new Promise((resolve, reject) => {
            axios
                .get(`${this.root}api/workflows`)
                .then(response => {
                    let workflows = response.data;
                    workflows.forEach(workflow => {
                        this._addAttributes(workflow);
                    });
                    resolve(workflows);
                })
                .catch(e => {
                    reject(this._errorMessage(e));
                });
        });
    }

    updateWorkflow(id, data) {
        return new Promise((resolve, reject) => {
            axios
                .put(`${this.root}api/workflows/${id}`, data)
                .then(response => {
                    resolve(response.data);
                })
                .catch(e => {
                    reject(this._errorMessage(e));
                });
        });
    }

    _addAttributes(workflow) {
        const Galaxy = getGalaxyInstance();
        workflow.shared = workflow.owner !== Galaxy.user.get("username");
        workflow.description = "Not available";
        if (workflow.annotations && workflow.annotations.length > 0) {
            const description = workflow.annotations[0].trim();
            if (description) {
                workflow.description = description;
            }
        }
    }

    _errorMessage(e) {
        let errorMessage = "Request failed.";
        if (e.response) {
            errorMessage = e.response.data.err_msg || `${e.response.statusText} (${e.response.status})`;
        }
        return errorMessage;
    }
}
