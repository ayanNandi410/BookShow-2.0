<template>
        <!-- Filter Modal -->
        <div class="modal fade" id="filterModal" data-bs-backdrop="static"
    data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="filterModalLabel">Filter Shows</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="post" action="/user/filterShows">

            <div class="modal-body" id="filterModalBody">
            <div class="container">

                <div class="row mb-3">
                <div class="col-12">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Tags</span>
                        <div class="form-control">
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagAction" name="tags" value="Action">
                                <label class="form-check-label" for="Action"> Action</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagThriller" name="tags" value="Thriller">
                                <label for="Thriller" class="form-check-label"> Thriller</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagComedy" name="tags" value="Comedy">
                                <label for="Comedy" class="form-check-label"> Comedy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagHorror" name="tags" value="Horror">
                                <label class="form-check-label" for="Horror"> Horror</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagMystery" name="tags" value="Mystery">
                                <label for="Mystery" class="form-check-label"> Mystery</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagFantasy" name="tags" value="Fantasy">
                                <label for="Fantasy" class="form-check-label"> Fantasy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagDrama" name="tags" value="Drama">
                                <label for="Drama" class="form-check-label"> Drama</label>    
                            </div>
                        </div>
                    </div>
                </div>
                <div id="tagCheck" class="invalid-feedback">&emsp;One tag must be selected</div>
                </div>

                <div class="row mb-3">
                <div class="col-12">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Languages</span>
                        <div class="form-control">
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangEnglish" name="languages" value="English">
                                <label class="form-check-label" for="English"> English</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangHindi" name="languages" value="Hindi">
                                <label for="Hindi" class="form-check-label"> Hindi</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangBengali" name="languages" value="Bengali">
                                <label for="Bengali" class="form-check-label"> Bengali</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangTamil" name="languages" value="Tamil">
                                <label class="form-check-label" for="Tamil"> Tamil</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangTelegu" name="languages" value="Telegu">
                                <label for="Telegu" class="form-check-label"> Telegu</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangMalayalam" name="languages" value="Malayalam">
                                <label for="Malayalam" class="form-check-label"> Malayalam</label>    
                            </div>
                        </div>
                    </div>
                </div>
                <div id="langCheck" class="invalid-feedback">&emsp;One Language must be selected</div>
            </div>

            <div class="col-12 col-sm-8 mb-3">
                <label for="userRating" class="form-label">Rating (greater than) <span id="ratingValue" class="badge bg-primary text-white" on="changeColour();">5</span></label>
                <input type="range" class="form-range" min="0" max="10" value="5" step="1" 
                name="userRating" id="userRating" onchange="updateRating(this.value);" required>
            </div>
            
            <div class="col-12 mb-3">
                <label for="runningShows" class="form-radio-label">Display only running shows? </label>
                <input type="radio" class="form-radio-input" name="runShows" value="yes" checked> Yes
                &emsp14;<input type="radio" class="form-radio-input" name="runShows" value="no"> No
            </div>
            <br/>

            </div>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" id="filterBt" class="btn btn-primary">Filter</button>
            </div>
            </form>
        </div>
        </div>
    </div>
</template>