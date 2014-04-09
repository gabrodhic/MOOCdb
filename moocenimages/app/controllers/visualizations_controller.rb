class VisualizationsController < ApplicationController
  before_filter :authenticate_user!, :only => [:new]
  
  def index
    tags = Tag.all
    @tags_hash = {}
    tags.each do |tag|
      visualizations = Visualization.where(:tag_id => tag.id)
      @tags_hash[tag.name] = visualizations
    end
  end

  def new
    @visualization = Visualization.new
  end

  def create
    visualization = Visualization.create(params[:visualization])
    visualization.update(:user_id => current_user.id)
    redirect_to '/new_viz_step_2?viz_id=' + visualization.id.to_s
  end
  
  def new_step_2
    @viz_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
  end

  def create_step_2
    viz_id = Integer(params[:viz_id])
    offerings = params[:offering][:name].split(',')
    # TODO: make this work with more than one offering
    offering = Offering.create(params[:offering].merge({:visualization_id => viz_id}))

    tags = Tag.where(:name => params[:tag])

    if tags.length > 0
      tag = tags[0]
    else
      tag = Tag.create(:name => params[:tag])
    end

    Visualization.find(viz_id).update(:tag_id => tag.id)
    redirect_to '/new_viz_step_3?viz_id=' + params[:viz_id] + '&offering_id=' + offering.id.to_s
  end

  def new_step_3
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_3
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_4?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_4
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_4
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_5?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_5
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_5
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_6?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_6
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_6
    @upload = Upload.create(params[:upload])
    redirect_to '/visualizations/' + params[:upload][:visualization_id]
  end

  def show
    @visualization = Visualization.find(params[:id])
    @offering = @visualization.offerings.first
  end

  def get_upload
    viz_step = params[:visualization_step_id]
    begin
      script = nil
      visualization = Visualization.find(params[:visualization_id])
      if viz_step == 2
        script = visualization.data_extraction_script
        script_name = visualization.data_extraction_script_file_name
      elsif viz_step == 4
        script = visualization.data_aggregation_script
        script_name = visualization.data_aggregation_script_file_name
      elsif viz_step == 6
        script = visualization.data_to_visualization_script
        script_name = visualization.data_to_visualization_script_file_name
      else
        begin
          offering = visualization.offerings.find(params[:offering_id])
          script = offering.public_data
          script_name = offering.public_data_file_name
        rescue ActiveRecord::RecordNotFound => e
          render :json => {:contents => "No offerings found for this visualization", :file_name => "File not Found"}
        end
      end

      if script.nil?
        render :json => {:contents => "No offerings found for this visualization", :file_name => "File not Found"}
      end

      script_contents = File.open(script.path).read

      response = {:contents => script_contents, :file_name => script_name}

    rescue ActiveRecord::RecordNotFound => e
      response = {:contents => "This file could not be read.", :file_name => "File Not Found"}
    end
    respond_to do |format|
      format.json {render :json => response}
    end
  end

  def get_zip
    require 'zip'
    require 'uri'

    visualization = Visualization.find(params[:visualization_id])
    offering = visualization.offerings.find(params[:offering_id])

    zipfile_name = '/zips/' + offering.name + '_' + visualization.name + '.zip'
    zipfile_path = 'public' + zipfile_name
    File.delete(zipfile_path) if File.exist?(zipfile_path)

    Zip::File.open(zipfile_path, Zip::File::CREATE) do |zipfile|
      zipfile.add(visualization.data_extraction_script_file_name, visualization.data_extraction_script.path)
      zipfile.add(visualization.data_aggregation_script_file_name, visualization.data_aggregation_script.path)
      zipfile.add(visualization.data_to_visualization_script_file_name, visualization.data_to_visualization_script.path)
      zipfile.add(offering.public_data_file_name, offering.public_data.path)
    end
    File.chmod(0644, zipfile_path)

    redirect_to URI.encode(zipfile_name)
  end
end
